from fastapi import APIRouter

order_router = APIRouter(prefix="/pedidos", tags=['roteador_edidos']) #definindo que todas as rotas aqui vai ficar dentro de order

@order_router.get("/") #ex: dominio.com/pedido
async def pedidos():
    return {"mensagem":"acessou a rota de pedidos"}