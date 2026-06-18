from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from dependecies import pegar_sessao
from schemas import PedidoSchema 
from models import pedido



order_router = APIRouter(prefix="/pedidos", tags=['roteador_edidos']) #definindo que todas as rotas aqui vai ficar dentro de order

@order_router.get("/") #ex: dominio.com/pedido
async def pedidos():
    return {"mensagem":"acessou a rota de pedidos"}



#criar um pedido em si
@order_router.post("/pedido")
async def criar_pedido(pedido_schema:PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"pedido feito com sucesso, id do pedido {pedido_schema.usuario}"}