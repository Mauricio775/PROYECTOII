from fastapi import APIRouter, HTTPException, Request, Query
from typing import Optional
from models.inventory import Inventory
from controllers.inventory import (
    create_inventory,
    get_inventory,
    get_inventory_id,
    update_id
)
from utils.security import validateadmin

router = APIRouter(tags=["inventory"])


@router.post("/inventory", response_model=Inventory)
@validateadmin
async def create_new_inventory(request: Request, inventory_data: Inventory):
    result = await create_inventory(inventory_data, request.state.id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result["data"]


@router.get("/{inventory_id}", response_model=Inventory)
@validateadmin
async def get_id_inventory(request: Request, inventory_id: str):
    return await get_inventory_id(inventory_id)

@router.get("/inventory", response_model=list[Inventory])
async def get_inventory_endpoint(
    request: Request,
    filtro: Optional[str] = Query(default=None, description="Filtrar por descripción del Inventario")
):
    return await get_inventory(filtro)

@router.put("/inventory/{inventory_id}", response_model=Inventory)
@validateadmin
async def update(inventory_id: str, update_data: Inventory, request: Request):
    return await update_id(inventory_id, update_data)






