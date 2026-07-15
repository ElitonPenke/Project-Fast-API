from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from dependecies import pegar_sessao,verificar_token
from schemas import PedidoSchema 
from models import pedido, user

#eu posso passar o parametro de um usuario estar logado em cada uma das minhas rotas, ou simplesmente colocar essa restriçao diretamente no meu router

order_router = APIRouter(prefix="/pedidos", tags=['roteador_edidos'], dependencies=[Depends(verificar_token)]) #definindo que todas as rotas aqui vai ficar dentro de order

#porem n consigo utilizar os resultados das funções dosparametros colocando aqui no dependecies[], tipo, criar_pedido, parametro session: ... de retorna uma seção em si e eu uso ela, aqui em cima n da

@order_router.get("/") #ex: dominio.com/pedido
async def pedidos():
    return {"mensagem":"acessou a rota de pedidos"}



#criar um pedido em si
@order_router.post("/pedido")
async def criar_pedido(pedido_schema:PedidoSchema, session: Session = Depends(pegar_sessao)):
   
    novo_pedido = pedido(usuario=pedido_schema.usuario)
   
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"pedido feito com sucesso, id do pedido {novo_pedido.id}"}

#calcelar um pedido
#id_pedido, parametro na rota é um do tipo url
#id_pedido, parametro na função é do tipo body

@order_router.post("/pedidpo/calcelar/{id_pedido}") # 'id_pedido' é um parametro para a rota 

async def cancelar_pedido (id_pedido: int,session: Session = Depends(pegar_sessao),usuario:user = Depends(verificar_token)) : # seu eu passei um parametro no rota, obrigatoriamente preciso passar na função
    #vai executar na minha tabela pedido aonde esta filtrando que a coluna id seja igual ao meu id_pedido passado como parametro na função
    Pedido=session.query(pedido).filter(pedido.id==id_pedido).first() #primeiro(boa pratica)
    
    if not Pedido:#se n exsite esse pedido
        raise HTTPException(status_code=400, detail='pedido n encontrado !')
    
    
    #se o usuario n é admin e também n é o dono do pedido, da erro
    if not usuario.admin and usuario.id != Pedido.usuario:
        raise HTTPException(status_code=401,detail='vc n tem autorização para calcelar esse pedido')
    
    
    #se exsite o pedido ele vai ser cancelado
    Pedido.status="CALCELADO"
    
    #precisamdos apenas um commit, visto que n estamos adicionadno nada novo em si na secão, somente alteranod algo que ja exsite la dentro(db)
    session.commit()
    
    #essa rota aqui por si so ja esta pronta, porem vou colocar uma mensagem dizerndo que deu certo
    
    return {    #ao eu carregar o id do pedido que teoricamente ja foi fechado antes no commit, eu forço o software carregar toda a minha isntancia do pedido, assim ele tras td novamente assim posibilitando trazer o pedido:{}
        "mensagem":f' Deu certo o cancelamento do pedido {Pedido.id}',
        "pedido":Pedido # um resumo do pedido cancelado
    }
    
    
"""1° verificamos se o o cara esta logado no sistema com o verificar_token
2° verificamos se o pedido existe
3° verficamos se o user com o token e tals, é admin ou é o dono do pedido
4° ai muda o pedido comita na secao
5° retorna os detalhes do pedido cancelado"""