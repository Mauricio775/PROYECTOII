import logging
from fastapi import HTTPException
from models.book import Book
from utils.mongodb import get_collection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_book(book: Book) -> Book:
    try:
        coll = get_collection("book")

        book_dict = book.model_dump(exclude={"id"})
        result = coll.insert_one(book_dict)

        book.id = str(result.inserted_id)
        return book

    except Exception as e:
        logger.error(f"Error al crear el libro: {e}")
        raise HTTPException(status_code=500, detail="Error al crear el libro")
