from fastapi import APIRouter
from models.book import Book
from controllers.book import create_book

router = APIRouter(prefix="/book", tags=["Book"])

@router.post("/")
async def post_book(book: Book):
    return await create_book(book)
