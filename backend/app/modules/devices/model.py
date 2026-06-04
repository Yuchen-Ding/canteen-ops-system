from sqlalchemy import BigInteger, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.common.models import Base


class Device(Base):
    __tablename__ = "devices"
    __table_args__ = {"schema": "canteen_ops"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    device_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    device_name: Mapped[str] = mapped_column(String(120), nullable=False)
    canteen_id: Mapped[int] = mapped_column(ForeignKey("canteen_ops.canteens.id"), nullable=False)
    stall_id: Mapped[int | None] = mapped_column(ForeignKey("canteen_ops.stalls.id"))
    device_type: Mapped[str] = mapped_column(String(30), nullable=False)
    ip_address: Mapped[str | None] = mapped_column(String(60))
    location: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="OFFLINE")
    last_heartbeat_time: Mapped[object | None] = mapped_column(DateTime(timezone=True))
    remark: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
