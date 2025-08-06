from bson import ObjectId
from fastapi import HTTPException
from models.orderdetails import OrderDetails
from utils.mongodb import get_collection
from pipelines.orderdetails_pipelines import get_order_details_grouped_pipeline
order_details_collection = get_collection("orderdetails")

async def create_order_detail(data: OrderDetails) -> OrderDetails:
    try:
        inventory_collection = get_collection("inventory")
        if not ObjectId.is_valid(data.id_inventory):
            raise HTTPException(status_code=400, detail="ID de inventario inválido")
        inventory = inventory_collection.find_one({"_id": ObjectId(data.id_inventory)})
        if not inventory:
            raise HTTPException(status_code=404, detail="Inventario no encontrado")

        orders_collection = get_collection("orders")
        if not ObjectId.is_valid(data.id_order):
            raise HTTPException(status_code=400, detail="ID de orden inválido")
        order = orders_collection.find_one({"_id": ObjectId(data.id_order)})
        if not order:
            raise HTTPException(status_code=404, detail="Orden no encontrada")

        detail_dict = data.model_dump(exclude={"id"})
        inserted = order_details_collection.insert_one(detail_dict)
        data.id = str(inserted.inserted_id)
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear detalle de orden: {str(e)}")


async def get_order_details_grouped() -> list[dict]:
    try:
        pipeline = get_order_details_grouped_pipeline()
        result = list(order_details_collection.aggregate(pipeline))

        if not result:
            raise HTTPException(status_code=404, detail="No se encontraron detalles de orden")

        for doc in result:
            doc["id_order"] = doc.pop("_id")  # Renombrar para consistencia

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener detalleS de la orden"+ str(e))