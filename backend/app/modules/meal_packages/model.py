from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.common.models import Base


class MealPackage(Base):
    __tablename__ = "meal_packages"
    __table_args__ = {"schema": "canteen_ops"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    package_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    stall_id: Mapped[int] = mapped_column(ForeignKey("canteen_ops.stalls.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    package_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="ACTIVE")
    remark: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class MealPackageItem(Base):
    __tablename__ = "meal_package_items"
    __table_args__ = (
        UniqueConstraint("package_id", "dish_id"),
        {"schema": "canteen_ops"},
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    package_id: Mapped[int] = mapped_column(ForeignKey("canteen_ops.meal_packages.id"), nullable=False)
    dish_id: Mapped[int] = mapped_column(ForeignKey("canteen_ops.dishes.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
