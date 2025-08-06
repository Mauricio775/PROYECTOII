from fastapi import APIRouter, Request
from models.orderdetails import OrderDetails
from controllers.orderdetails import (
    create_order_detail,
    get_order_details_grouped
)
from utils.security import validateadmin

router = APIRouter(tags=["Orderdetails"])


@router.post("/orderdetails", response_model=OrderDetails)
@validateadmin
async def create_order_detail_endpoint(request: Request, data: OrderDetails) -> OrderDetails:
    return await create_order_detail(data)

@router.get("/orderdetails", response_model=list[dict])
@validateadmin
async def get_grouped(request: Request) -> list[dict]:
    return await get_order_details_grouped()