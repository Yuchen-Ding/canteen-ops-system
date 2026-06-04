from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.pos.schema import EmployeeCardPaymentRequest, VisitorQrPaymentRequest
from app.modules.pos.service import create_employee_card_payment, create_visitor_qr_payment

router = APIRouter(prefix="/api/v1/pos", tags=["pos"])


@router.post("/employee-card-payment")
async def employee_card_payment(payload: EmployeeCardPaymentRequest, db: AsyncSession = Depends(get_db)) -> dict:
    return await create_employee_card_payment(db, payload)


@router.post("/visitor-qr-payment")
async def visitor_qr_payment(payload: VisitorQrPaymentRequest, db: AsyncSession = Depends(get_db)) -> dict:
    return await create_visitor_qr_payment(db, payload)
