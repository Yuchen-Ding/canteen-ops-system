from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.ai.schema import AiChatRequest
from app.modules.ai.service import chat, get_latest_session

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])


@router.get("/sessions/latest")
async def latest_session_api(db: AsyncSession = Depends(get_db)) -> dict:
    return await get_latest_session(db)


@router.post("/chat")
async def ai_chat_api(payload: AiChatRequest, db: AsyncSession = Depends(get_db)) -> dict:
    return await chat(db, payload.session_id, payload.message)
