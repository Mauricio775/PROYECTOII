import logging
from fastapi import HTTPException
from models.book import Book
from utils.mongodb import get_collection
from bson import ObjectId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from pipelines.book_pipelines import (
    get_book_pipeline,
    validate_book_assigned_pipeline
    
)
coll = get_collection("book")

async def create_book(book: Book) -> Book:
    try:

        exist_book = coll.find_one({"description": book.description})
        if exist_book:
            raise HTTPException(status_code=400, detail="Book already exists")

        book_dict = book.model_dump(exclude={"id"})
        inserted = coll.insert_one(book_dict)
        book.id = str(inserted.inserted_id)
        return book
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el libro: {str(e)}")
    
    
async def get_book() -> list:
    try:
        
        pipeline = get_book_pipeline()
        book = list(coll.aggregate(pipeline))
        return book
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    
async def get_book_id(book_id:str)-> Book:
    try:
        doc = coll.find_one({"_id": ObjectId(book_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        
        doc['id'] = str(doc['_id'])
        del doc['_id']
        return Book(**doc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error book: {str(e)}")
        
async def update_book(book_id: str, book: Book) -> Book:
    try:
        # 1) Evitar duplicado contra el propio documento
        dup = coll.find_one({
            "_id": {"$ne": ObjectId(book_id)},
            "description": book.description
        })
        if dup:
            raise HTTPException(status_code=400, detail="Book already exists")

        # 2) Actualizar
        res = coll.update_one(
            {"_id": ObjectId(book_id)},
            {"$set": book.model_dump(exclude={"id"})}
        )

        # matched_count verifica existencia; modified_count puede ser 0 si no cambió nada
        if res.matched_count == 0:
            raise HTTPException(status_code=404, detail="Libro no encontrado")

        # 3) Devolver el documento actualizado para cumplir response_model=Book
        doc = coll.find_one({"_id": ObjectId(book_id)})
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        return Book(**doc)

    except HTTPException:
        # No convertir 400/404 en 500
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando: {str(e)}")    
    
    
async def deactivate_book(book_id: str) -> dict:
    try:
        pipeline= validate_book_assigned_pipeline(book_id)
        assigned = list(coll.aggregate(pipeline))
        
        if assigned is None:
            raise HTTPException(status_code=404, detail="Book not found")
        
        if assigned[0]["number_of_products"] > 0:
            coll.update_one(
                {"_id": ObjectId(book_id)},
                {"$set": {"active": False}}
            )
            return {"message": "Book is assigned to products and has been deactivated"}
        
        else: 
            coll.delete_one({"_id": ObjectId(book_id)})
            return {"message": "Catalog type deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deactivating Book: {str(e)}")
