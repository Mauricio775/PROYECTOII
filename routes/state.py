
from fastapi import APIRouter, Request, Query
from models.state import CreateState, State
from typing import Optional
from controllers.state import (
    create_state_for_payment,
    update_state_for_payment,
)
from utils.security import validateuser, validateadmin

router = APIRouter(tags=["states"])

@router.post("/payments/{payment_id}/state", response_model=State)
@validateadmin
async def add_state_to_payment(request: Request, payment_id: str, state_data: CreateState):
    return await create_state_for_payment(payment_id, state_data)


@router.put("/payments/{payment_id}/state", response_model=State)
@validateadmin
async def update_state_to_payment(request: Request, payment_id: str, state_data: CreateState):
    return await update_state_for_payment(payment_id, state_data)
