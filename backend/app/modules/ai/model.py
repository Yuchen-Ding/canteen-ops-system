from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.common.models import Base


class AiChatSession(Base):
    __tablename__ = "ai_chat_sessions"
    __table_args__ = {"schema": "canteen_ops"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    session_no: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class AiChatMessage(Base):
    __tablename__ = "ai_chat_messages"
    __table_args__ = {"schema": "canteen_ops"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("canteen_ops.ai_chat_sessions.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
