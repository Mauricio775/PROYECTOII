from fastapi import APIRouter, HTTPException, Request, Query
from typing import Optional
from models.inventory import Inventory
from controllers.inventory import (
    create_inventory,
    get_inventory,
    get_inventory_id,
    update_id,
    deactivate_inventory
)
from utils.security import validateadmin, validateuser

router = APIRouter(tags=["inventory"])


@router.post("/inventory", response_model= Inventory)
@validateuser
async def create_inventory_endpoint(request: Request, inventory: Inventory) -> Inventory:
    """Crear un nuevo Inventario"""
    return await create_inventory(inventory)

@router.get("/inventory", response_model=list[Inventory])
@validateuser
async def get_inventory_endpoint(request: Request):
    """Obtener todos los inventarios"""
    return await get_inventory()

@router.get("/inventory/{inventory_id}", response_model=Inventory)
@validateuser
async def get_id_inventory(request: Request, inventory_id: str):
    return await get_inventory_id(inventory_id)


@router.put("/inventory/{inventory_id}", response_model=Inventory)
@validateuser
async def update(inventory_id: str, update_data: Inventory, request: Request):
    return await update_id(inventory_id, update_data)

@router.delete("/inventory/{inventory_id}", response_model=Inventory)
@validateuser
async def deactivate_inventory_endpoint(request: Request,inventory_id: str) -> Inventory:
    """Desactivar un Inventario"""
    return await deactivate_inventory(inventory_id)





