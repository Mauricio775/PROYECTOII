import os
import uvicorn
from fastapi import FastAPI, Request


from controllers.users import create_user, login
from models.users import User
from models.login import Login

from utils.security import validateuser
from utils.security import validateadmin


from routes.book import router as book_router
from routes.reviews import router as reviews_router
from routes.inventory import router as inventory_routes
from routes.payments import router as payments_routes
from routes.state import router as state_routes
from routes.orders import router as orders_routes
from routes.payments_type import router as payments_type_router
from routes.paymenthistory import router as paymenthistory_router
from routes.orderdetails import router as orderdetails_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"version": "0.0.0"}

@app.get("/health")
def health_check():
    try:
        return {
            "status": "healthy",
            "timestamp": "2025-01-31",
            "service": "libros-proyecto",
            "environment": "production"
        }
    except Exception as e:
        return {"status": "unhealthy", "error":str(e)}

@app.get("/ready")
def readiness_check():
    try:
        from utils.mongodb import test_connection
        db_status = test_connection()
        return {
            "status": "ready"  if db_status else "not_ready",
            "database": "connected" if db_status else "disconnected",
            "service": "libros-proyecto"
        }
    except Exception as e:
        return {"status": "not_ready", "error": str(e)}

@app.post("/users")
async def create_user_endpoint(user: User) -> User:
    return await create_user(user)

@app.post("/login")
async def login_access(l: Login) -> dict:
    return await login(l)

@app.get("/exampleadmin")
@validateadmin
async def example_admin(request: Request):
    return {
        "message": "This is an example admin endpoint."
        , "admin": request.state.admin
    }

@app.get("/exampleuser")
@validateuser
async def example_user(request: Request):
    return {
        "message": "This is an example user endpoint."
        ,"email": request.state.email
    }

app.include_router(reviews_router)
app.include_router(book_router)
app.include_router(inventory_routes)
app.include_router(payments_routes)
app.include_router(state_routes)
app.include_router(orders_routes)
app.include_router(payments_type_router)
app.include_router(paymenthistory_router)
app.include_router(orderdetails_router)


if __name__== "_main_":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")