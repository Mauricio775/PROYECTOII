from bson import ObjectId
from fastapi import HTTPException

from models.payments_type import PaymentsType
from utils.mongodb import get_collection
from pipelines.payments_type_pipelines import (
    get_all_payments_type_pipeline,
    get_payment_type_by_id_pipeline
)

payments_type_collection = get_collection("payments_type")

async def payments_type_create(payments_type: PaymentsType) -> PaymentsType:
    try:
        payments_collection = get_collection("payments")
        exist_payments = payments_collection.find_one({"_id": ObjectId(payments_type.id_payments)})
        if not exist_payments:
            raise HTTPException(status_code=400, detail="El ID de payment no existe")
    
        payments_type_dict = payments_type.model_dump(exclude={"id"})
        inserted = payments_type_collection.insert_one(payments_type_dict)
        payments_type.id = str(inserted.inserted_id)
        return payments_type
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def get_payments_type_id(payments_type_id: str) -> dict:
    try:
        payments_type = payments_type_collection.find_one({"_id": ObjectId(payments_type_id)})
        if not payments_type:
            raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")

        payments_type["id"] = str(payments_type["_id"])
        del payments_type["_id"]
        return payments_type
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def get_payments_type() -> list[dict]:
    try:
        pipeline = get_all_payments_type_pipeline()
        payments_type_result = list(payments_type_collection.aggregate(pipeline))
        
        if not payments_type_result:
            raise HTTPException(status_code=404, detail="Tipos de pago no encontrados")

        return payments_type_result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener tipos de pago: " + str(e))
        
async def delete_payments_type(payments_type_id: str) -> dict:
    try:
        result = payments_type_collection.delete_one({"_id": ObjectId(payments_type_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")

        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
