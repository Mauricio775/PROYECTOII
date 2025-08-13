import logging
from typing import Optional
from bson import ObjectId
from fastapi import HTTPException
from models.inventory import Inventory
from utils.mongodb import get_collection 
from pipelines.inventory_pipelines import get_inventory_with_book_pipeline
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

inventory_collection = get_collection("inventory")
book_collection = get_collection("book")
########################
async def create_inventory(inventory: Inventory) -> Inventory:
    try:
        dup = inventory_collection.find_one({
            "id_book": inventory.id_book,
            "name": inventory.name
        })
        if dup:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un inventario con ese nombre para este libro"
            )

        inventory_dict = inventory.model_dump(exclude={"id"})
        result = inventory_collection.insert_one(inventory_dict)
        inventory.id = str(result.inserted_id)
        return inventory

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

        

async def get_inventory() -> list[Inventory]:
    try:
        pipeline = get_inventory_with_book_pipeline()
        docs = list(inventory_collection.aggregate(pipeline))
        
        result = []
        for doc in inventory_collection.find({}):   
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            result.append(Inventory(**doc))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error services: {str(e)}")
    

async def get_inventory_id(inventory_id: str) -> Inventory:
    if not ObjectId.is_valid(inventory_id):
        raise HTTPException(status_code=400, detail="ID de inventario inválido")

    try:
        doc = inventory_collection.find_one({"_id": ObjectId(inventory_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Inventario no encontrado")

        doc["id"] = str(doc["_id"])
        del doc["_id"]
        return Inventory(**doc)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")



async def update_id(inventory_id: str, update_data: Inventory) -> Inventory:
    try:
        
        update_dict = update_data.model_dump(exclude_unset=True, exclude={"id"})

        result = inventory_collection.update_one({"_id": ObjectId(inventory_id)}, {"$set": update_dict})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Inventario no encontrado")

        update_data.id = inventory_id
        return update_data
    except Exception as e:
        logger.error(f"Error al actualizar inventario: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar inventario")


async def deactivate_inventory(inventory_id: str) -> Inventory:
    try:
        result = inventory_collection.update_one(
            {"_id": ObjectId(inventory_id)},
            {"$set": {"active": False}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Inventory no encontrado")

        return await get_inventory_id(inventory_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error desactivando Catalogo: {str(e)}")