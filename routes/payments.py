from fastapi import APIRouter, HTTPException, Request
from models.payments import Payment
from controllers.payments import (
    create_payment,
    get_payments_order,
    update_payment,
    delete_payment
    
    
)

from utils.security import validateadmin , validateuser

router = APIRouter(tags=["payments"])

@router.post("/{order_id}/payments", response_model=Payment )
@validateadmin
async def create_new_payment(order_id:str, request : Request, payment_data: Payment):
    return await create_payment(order_id, payment_data)


@router.get("/{order_id}/payments", response_model=list[Payment])
@validateadmin
async def get_payments(order_id: str, request:Request):
    return await get_payments_order(order_id)

@router.put("/payments/{payment_id}", response_model=Payment)
@validateadmin
async def update_id_payment(request: Request, payment_id: str, payment_data: Payment) -> Payment:
    return await update_payment(payment_id, payment_data)

@router.delete("/payments/{payment_id}")
@validateadmin
async def delete_id_payment(payment_id: str, request: Request):
    return await delete_payment(payment_id)  # sin await





