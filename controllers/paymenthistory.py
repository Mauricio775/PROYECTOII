from fastapi import HTTPException
from bson import ObjectId
from models.paymenthistory import PaymentHistory
from utils.mongodb import get_collection
from pipelines.paymenthistory_pipelines import get_all_payment_history_pipeline, get_payment_history_by_id_pipeline

paymenthistory_collection = get_collection("paymenthistory")

async def create_paymenthistory(paymenthistory: PaymentHistory) -> PaymentHistory:
    try:
        coll_payments = get_collection("payments")
        exist_payments = coll_payments.find_one({"_id": ObjectId(paymenthistory.id_payments)})
        if not exist_payments:
            raise HTTPException(status_code=404, detail="Pago no encontrado")
        
        
        coll_paymentstypes = get_collection("payments_type")
        exist_paymentstypes = coll_paymentstypes.find_one({"_id": ObjectId(paymenthistory.id_payments_type)})
        if not exist_paymentstypes:
            raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")
        
        coll_states = get_collection("states")
        exist_states = coll_states.find_one({"_id": ObjectId(paymenthistory.id_state)})
        if not exist_states:
            raise HTTPException(status_code=404, detail="Estado no encontrado")
        
        paymenthistory_dict = paymenthistory.model_dump(exclude={"id"})
        inserted = paymenthistory_collection.insert_one(paymenthistory_dict)
        paymenthistory.id = str(inserted.inserted_id)
        return paymenthistory
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
async def get_paymenthistory() -> list[dict]:
    try:
        pipeline = get_all_payment_history_pipeline()
        paymenthistory_result = list(paymenthistory_collection.aggregate(pipeline))
        
        if not paymenthistory_result:
            raise HTTPException(status_code=404, detail="Error al obtener el Historial de pago")

        return paymenthistory_result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error Historial de Pago: " + str(e))
    
async def delete_paymenthistory(paymenthistory_id: str) -> dict:
    try:
        result = paymenthistory_collection.delete_one({"_id": ObjectId(paymenthistory_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Historial de pago no encontrado")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))