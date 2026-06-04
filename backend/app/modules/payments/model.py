from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.common.models import Base


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = {"schema": "canteen_ops"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    payment_no: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey("canteen_ops.orders.id"), unique=True, nullable=False)
    payment_method: Mapped[str] = mapped_column(String(30), nullable=False)
    payment_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    payment_status: Mapped[str] = mapped_column(String(30), nullable=False, default="PENDING")
    paid_at: Mapped[object | None] = mapped_column(DateTime(timezone=True))
    failure_reason: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
