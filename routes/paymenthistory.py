from fastapi import APIRouter, HTTPException, Request
from typing import List
from utils.security import validateadmin, validateuser
from models.paymenthistory import PaymentHistory
from controllers.paymenthistory import (
    create_paymenthistory,
    get_paymenthistory,
    delete_paymenthistory
)

router = APIRouter(prefix="/paymenthistory", tags=["Payment History"])

@router.post("/", response_model=PaymentHistory)
@validateadmin
async def create(request: Request ,data: PaymentHistory)  -> PaymentHistory:
    return await create_paymenthistory(data)

@router.get("/", response_model=dict)
@validateuser
async def get_all(request:Request)-> dict:
    return await get_paymenthistory()


@router.delete("/{payment_history_id}", response_model=dict)
@validateadmin
async def delete(request:Request , payment_history_id: str)-> None:
    return await delete_paymenthistory(payment_history_id)
