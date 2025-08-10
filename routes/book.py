from fastapi import APIRouter, Request
from models.book import Book
from controllers.book import (
    create_book,
    get_book,
    get_book_id,
    update_book,
    desactivate_book
)
from utils.security import validateuser

router = APIRouter(tags=["Book"])

@router.post("/book")
async def post_book(book: Book):
    return await create_book(book)


@router.get("/book", response_model=list)
@validateuser
async def get_book_endpoint(request: Request) -> list:
    return await get_book()

@router.get("/book/{book_id}", response_model=Book)
@validateuser
async def get_book_id_endpoint(request: Request, book_id: str) -> Book:
    return await get_book_id(book_id)

@router.put("/book/{book_id}", response_model=Book)
@validateuser
async def update_book_endpoint(request: Request, book_id: str, book: Book) -> Book:
    return await update_book(book_id, book)

@router.delete("/book/{book_id}", response_model=dict)
@validateuser
async def deactivate_book_endpoint(request: Request, book_id: str) -> dict:
    return await desactivate_book(book_id)