import json
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.ai.model import AiChatMessage, AiChatSession
from app.modules.ai.provider import request_deepseek
from app.modules.monitoring.service import get_canteen_overview
from app.modules.reports.service import (
    REPORT_TIMEZONE,
    get_dashboard_report,
    get_monthly_report,
    get_yearly_report,
)


def _session_no() -> str:
    return f"AI{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}{uuid4().hex[:6].upper()}"


def _message_dict(message: AiChatMessage) -> dict:
    return jsonable_encoder(
        {
            "id": message.id,
            "session_id": message.session_id,
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at,
        }
    )


async def _create_session(db: AsyncSession) -> AiChatSession:
    session = AiChatSession(session_no=_session_no(), title="食堂运营助手会话")
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def _get_messages(db: AsyncSession, session_id: int, limit: int = 50) -> list[AiChatMessage]:
    result = await db.execute(
        select(AiChatMessage)
        .where(AiChatMessage.session_id == session_id)
        .order_by(AiChatMessage.id.desc())
        .limit(limit)
    )
    return list(reversed(result.scalars().all()))


async def get_latest_session(db: AsyncSession) -> dict:
    session = await db.scalar(select(AiChatSession).order_by(AiChatSession.updated_at.desc()).limit(1))
    if not session:
        session = await _create_session(db)
    messages = await _get_messages(db, session.id)
    return jsonable_encoder(
        {
            "session": {
                "id": session.id,
                "session_no": session.session_no,
                "title": session.title,
                "created_at": session.created_at,
                "updated_at": session.updated_at,
            },
            "messages": [_message_dict(message) for message in messages],
        }
    )


async def _build_operational_context(db: AsyncSession) -> dict:
    now = datetime.now(REPORT_TIMEZONE)
    return {
        "generated_at": now.isoformat(),
        "monitoring_overview": await get_canteen_overview(db),
        "today_report": await get_dashboard_report(db),
        "current_month_report": await get_monthly_report(db, now.strftime("%Y-%m")),
        "current_year_report": await get_yearly_report(db, now.strftime("%Y")),
    }


async def chat(db: AsyncSession, session_id: int | None, user_message: str) -> dict:
    session = await db.get(AiChatSession, session_id) if session_id else None
    if session_id and not session:
        raise HTTPException(status_code=404, detail="AI 会话不存在。")
    if not session:
        session = await _create_session(db)

    user_record = AiChatMessage(session_id=session.id, role="USER", content=user_message.strip())
    session.updated_at = datetime.now(timezone.utc)
    db.add(user_record)
    await db.commit()

    context = await _build_operational_context(db)
    history = await _get_messages(db, session.id, limit=12)
    system_prompt = (
        "你是企业食堂运营助手。你只能依据提供的结构化食堂运营上下文回答，"
        "不得生成或建议执行 SQL，不得修改任何业务数据。"
        "回答使用中文，优先给出明确数字、对比和简短运营建议。"
        "如果问题与当前食堂运营数据无关，请回答：我主要基于当前食堂运营数据回答。"
        f"\n结构化运营上下文：{json.dumps(jsonable_encoder(context), ensure_ascii=False)}"
    )
    provider_messages = [{"role": "system", "content": system_prompt}]
    provider_messages.extend(
        {
            "role": "assistant" if message.role == "ASSISTANT" else "user",
            "content": message.content,
        }
        for message in history
        if message.role in {"USER", "ASSISTANT"}
    )

    answer = await request_deepseek(provider_messages)
    assistant_record = AiChatMessage(session_id=session.id, role="ASSISTANT", content=answer)
    session.updated_at = datetime.now(timezone.utc)
    db.add(assistant_record)
    await db.commit()
    messages = await _get_messages(db, session.id)
    return {
        "session_id": session.id,
        "answer": answer,
        "messages": [_message_dict(message) for message in messages],
    }
