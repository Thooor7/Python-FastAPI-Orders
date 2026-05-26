from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_session
from schemas import PedidoSchema
from models import Pedido

orders_router = APIRouter(prefix="/orders", tags=["orders"])

@orders_router.get("/")
async def get_orders():
    return {"message": "List of orders"}

@orders_router.post("/pedido")
async def create_order(pedido_schema: PedidoSchema, session: Session = Depends(get_session)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario_id)
    session.add(novo_pedido)
    session.commit()
    return {"message": "Order created", "order": pedido_schema}