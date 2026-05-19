# para executar a API: uvicorn main:app --reload

from fastapi import FastAPI

app = FastAPI()

from auth_routes import auth_router
from orders_routes import orders_router

app.include_router(auth_router)
app.include_router(orders_router)