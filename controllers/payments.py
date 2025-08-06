from models.payments import Payment
from fastapi import HTTPException
from utils.mongodb import get_collection
from bson import ObjectId
from datetime import datetime
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

payments_collection= get_collection("payments")

async def create_payment(order_id: str , payment_data: Payment) -> Payment:
    try: 
        orders_collection = get_collection("orders")
        order = orders_collection.find_one({"_id": ObjectId(order_id)})
        if not order:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        new_payment = Payment(state_method=payment_data.state_method, payment_date=datetime.utcnow(),amount=payment_data.amount, id_order=order_id )
        result = payments_collection.insert_one(new_payment.model_dump(exclude={"id"}))
        new_payment.id = str(result.inserted_id)
        
        return new_payment
    
    except Exception as e:
        raise HTTPException(status_code=500, detail= "Error al crear pago")

async def get_payments_order(order_id: str) -> list[Payment]:
    try:
        cursor = payments_collection.find({"id_order": order_id})
        return [Payment(**{**doc, "id": str(doc["_id"])}) for doc in cursor]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener pagos")

    
    
    
async def  update_payment(payment_id:str, payment_data: Payment) ->Payment:
    try:
        
        update_data = payment_data.model_dump(exclude_unset=True, exclude={"id"})
        
        result = payments_collection.update_one( { "_id": ObjectId(payment_id)} , { "$set": update_data} )
        
        if result.matched_count ==0:
            raise HTTPException(status_code= 404, detail= "Pago no encontrado")
        
        return Payment(id = payment_id, **update_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail= "Error al actualizar")
    
async def delete_payment(payment_id: str) -> dict:
    try:
        
        result = payments_collection.delete_one({"_id": ObjectId(payment_id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="El pago no fue encontrado")

        return {"message": "Pago eliminado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar pago")

