from datetime import datetime
from typing import Optional
import logging
from bson import ObjectId
from fastapi import HTTPException

from models.orders import Order
from utils.mongodb import get_collection


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

orders_collection = get_collection("orders")
users_collection = get_collection("users")

async def create_order(order_data: Order) -> Order:
    try:
        user_exists = users_collection.find_one({"_id": ObjectId(order_data.id_user)})
        if not user_exists:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except Exception:
        raise HTTPException(status_code=400, detail="Formato de ID de usuario inválido")

    order_dict = order_data.dict(exclude={"id"})
    order_dict["order_date"] = order_dict.get("order_date") or datetime.utcnow()

    result = orders_collection.insert_one(order_dict)
    return Order(**order_dict, id=str(result.inserted_id))


async def update_order(order_id: str, order_data: Order) -> Order:
    try:
        order_obj_id = ObjectId(order_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Formato de ID de orden inválido")

    try:
        user_obj_id = ObjectId(order_data.id_user)
    except Exception:
        raise HTTPException(status_code=400, detail="Formato de ID de usuario inválido")

    user_exists = users_collection.find_one({"_id": user_obj_id})
    if not user_exists:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_data = order_data.dict(exclude={"id"})
    update_data["order_date"] = update_data.get("order_date") or datetime.utcnow()

    result = orders_collection.update_one(
        {"_id": order_obj_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    return Order(**update_data, id=order_id)
