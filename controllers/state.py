from bson import ObjectId
from fastapi import HTTPException
from datetime import datetime
from models.state import State, CreateState
from utils.mongodb import get_collection
from typing import Optional
states_collection = get_collection("states")
payments_collection = get_collection("payments")


async def create_state_for_payment(payment_id: str, state_data: CreateState) -> State:
    try:
        # Validar ID de pago
        if not ObjectId.is_valid(payment_id):
            raise HTTPException(status_code=400, detail="ID de pago inválido")

        payment_exists = payments_collection.find_one({"_id": ObjectId(payment_id)})
        if not payment_exists:
            raise HTTPException(status_code=404, detail="Pago no encontrado")

        # Crear el documento de estado asociado al pago
        new_state = {
            "description": state_data.description,
            "payment_id": payment_id,
            "created_at": datetime.utcnow()
        }

        result = states_collection.insert_one(new_state)
        new_state["id"] = str(result.inserted_id)

        return State(**new_state)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear estado")
    


async def update_state_for_payment(payment_id: str, state_data: CreateState) -> State:
    try:
        if not ObjectId.is_valid(payment_id):
            raise HTTPException(status_code=400, detail="ID de pago inválido")

        payment_exists = payments_collection.find_one({"_id": ObjectId(payment_id)})
        if not payment_exists:
            raise HTTPException(status_code=404, detail="Pago no encontrado")

        existing_state = states_collection.find_one({"payment_id": payment_id})
        if not existing_state:
            raise HTTPException(status_code=404, detail="Estado no encontrado para este pago")

        states_collection.update_one(
            {"_id": existing_state["_id"]},
            {"$set": {
                "description": state_data.description,
                "updated_at": datetime.utcnow()
            }}
        )

        updated = states_collection.find_one({"_id": existing_state["_id"]})
        updated["id"] = str(updated["_id"])
        return State(**updated)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar estado")



