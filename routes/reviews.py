from fastapi import APIRouter, Request, HTTPException
from models.reviews import Review

from controllers.reviews import(
    create_review,
    get_reviews,
    reviews_update,
    reviews_delete
)

from utils.security import validateuser, validateadmin

router = APIRouter(tags=["Reviews"])


@router.post("/book/{bookId}/reviews")
@validateuser
async def create_new_review(
    request: Request,
    bookId: str,
    review_data:Review
):
    review_data.id_user = request.state.id
    review_data.id_book = bookId
    result = await create_review(review_data)
    return result


@router.get("/book/{bookId}/reviews", tags=["Reviews"])
@validateadmin
async def get_reviews_admin(
    request: Request,
    bookId: str
):
    return await get_reviews(bookId)

@router.put("/{review_id}", response_model=Review)
@validateadmin
async def review_update_admin(
    request:Request,
    review_id :str,
    review: Review
) -> Review:
    return await reviews_update(review_id,review)


@router.delete("/{review_id}", response_model=Review)
@validateadmin
async def review_delete_admin(
    request:Request,
    review_id :str,
) -> None:
    return await reviews_delete(review_id)




