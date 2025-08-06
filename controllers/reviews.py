import logging
from bson import ObjectId
from fastapi import HTTPException

from models.reviews import Review
from utils.mongodb import get_collection

logging.basicConfig(level=logging.INFO)    
logger = logging.getLogger(__name__)

reviews_collection = get_collection("reviews")

async def create_review(review: Review) -> Review:
    try:
        exist_review = reviews_collection.find_one({
            "id_user": review.id_user,
            "id_book": review.id_book
        })

        if exist_review:
            raise HTTPException(status_code=400, detail="Reseña ya existe")

        review_dict = review.model_dump(exclude={"id"})
        result = reviews_collection.insert_one(review_dict)
        review.id = str(result.inserted_id)
        return review

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    
async def get_reviews(book_id: str) -> list[Review]:
    try:
        
        cursor = reviews_collection.find({"id_book": book_id})
        reviews = []

        
        for doc in cursor:
            reviews.append(Review(**{**doc, "id": str(doc["_id"])}))

        return reviews

    except Exception as e:
        logger.error(f"Error al obtener reseñas del libro {book_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener reseñas del libro")


async def reviews_update(reviews_id : str, review: Review) -> Review:
    try:
        result = reviews_collection.update_one({"_id": ObjectId(reviews_id)}, {"$set": review.model_dump(exclude={"id"})})
        
        if result.modified_count == 0:
            raise HTTPException(status_code= 404, detail="Review no encontrada")
        
        review.id= reviews_id
        return review
    except Exception as e:
        raise HTTPException(status_code=500, detail =str(e))
    
async def reviews_delete(reviews_id: str) -> Review:
    try:
        result = reviews_delete.delete_one({"_id": ObjectId(reviews_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Review no encontrada")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    

