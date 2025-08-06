from fastapi import APIRouter, Request, Query
from typing import Optional
from models.orders import Order
from controllers.orders import (
    create_order,
    update_order
)
from utils.security import validateuser

router = APIRouter(tags=["Orders"])

@router.post("/order", response_model=Order)
@validateuser
async def create_new_order(request: Request, order_data: Order):
    return await create_order(order_data)



@router.put("/order/{order_id}", response_model=Order)
@validateuser
async def modify_order(request: Request, order_id: str, order_data: Order):
    return await update_order(order_id, order_data)

