from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.common.models import Base


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": "canteen_ops"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_no: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    canteen_id: Mapped[int] = mapped_column(ForeignKey("canteen_ops.canteens.id"), nullable=False)
    stall_id: Mapped[int] = mapped_column(ForeignKey("canteen_ops.stalls.id"), nullable=False)
    device_id: Mapped[int] = mapped_column(ForeignKey("canteen_ops.devices.id"), nullable=False)
    customer_type: Mapped[str] = mapped_column(String(30), nullable=False)
    employee_id: Mapped[int | None] = mapped_column(ForeignKey("canteen_ops.employees.id"))
    visitor_id: Mapped[int | None] = mapped_column(ForeignKey("canteen_ops.visitors.id"))
    visitor_name_snapshot: Mapped[str | None] = mapped_column(String(120))
    meal_type: Mapped[str] = mapped_column(String(30), nullable=False)
    original_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    subsidy_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    payable_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    payment_status: Mapped[str] = mapped_column(String(30), nullable=False, default="PENDING")
    order_status: Mapped[str] = mapped_column(String(30), nullable=False, default="CREATED")
    transaction_time: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    operator: Mapped[str | None] = mapped_column(String(120))
    remark: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = {"schema": "canteen_ops"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("canteen_ops.orders.id"), nullable=False)
    dish_id: Mapped[int | None] = mapped_column(ForeignKey("canteen_ops.dishes.id"))
    item_type: Mapped[str] = mapped_column(String(30), nullable=False)
    item_name_snapshot: Mapped[str] = mapped_column(String(120), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
