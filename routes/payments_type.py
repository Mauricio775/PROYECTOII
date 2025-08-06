from fastapi import APIRouter,HTTPException,Request
from typing import List
from utils.security import validateadmin, validateuser
from models.payments_type import PaymentsType
from controllers.payments_type import (
    payments_type_create,
    get_payments_type_id,
    delete_payments_type,
    get_payments_type
)

router = APIRouter(prefix="/paymentstype", tags=["Payments Type"])

@router.post("/", response_model=PaymentsType)
@validateadmin
async def create(request: Request,data: PaymentsType) -> PaymentsType:
    return await payments_type_create(data)

@router.get("/", response_model=List[PaymentsType])
@validateadmin
async def get_all(request:Request)-> dict:
    return await get_payments_type()

@router.get("/{payment_type_id}", response_model=PaymentsType)
@validateadmin
async def get_by_id(request : Request,payment_type_id: str)->PaymentsType:
    return await get_payments_type_id(payment_type_id)

@router.delete("/{payment_type_id}")
@validateadmin
async def delete(payment_type_id: str)-> None:
    return await delete_payments_type(payment_type_id)