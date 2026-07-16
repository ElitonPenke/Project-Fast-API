from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from dependecies import pegar_sessao,verificar_token
from schemas import PedidoSchema,ItemPedidoSchema #meus 'modelos' de como os dados devem ser
from models import pedido, user, Itempedido #as instancias, colunas,tabelas, do meu banco de dados em si

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

async def cancelar_pedido (id_pedido: int,session:Session = Depends(pegar_sessao),usuario:user = Depends(verificar_token)) : # seu eu passei um parametro no rota, obrigatoriamente preciso passar na função
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




#listar todos os meus pedidos
@order_router.get('/listar')
async def listar_pedidos(session:Session = Depends(pegar_sessao),usuario:user = Depends(verificar_token)):
    
    if usuario.admin ==False:  #mesma coisa --- if not usuario.admin
        raise HTTPException(status_code=401,detail='vc n tem autorização para listar os pedidos')
    else:                           #pedido importo do models
        todos_pedidos= session.query(pedido).all()
        return {
            'pedidos':todos_pedidos
        }
        
        
        
#editar um pedido
@order_router.post('/pedido/adicionar_item/{id_pedido}') #path
async def adicionar_item_pedido(id_pedido:int,
                                item_pedido_schema:ItemPedidoSchema,
                                session: Session = Depends(pegar_sessao),
                                usuario:user = Depends(verificar_token,)):
    
    Pedido=session.query(pedido).filter(pedido.id==id_pedido).first()
    if not Pedido:
        raise HTTPException(status_code=400,detail="pedido não enconctrado")
    
    if not usuario.admin and usuario.id != Pedido.usuario:
        raise HTTPException(status_code=401,detail="n tem autorização pra isso fi")
    
    #criar um item em si que vai ir no pedido seguinto o modelo ItemPedidoSchema
    item_pedido=Itempedido(item_pedido_schema.quantidade,item_pedido_schema.sabor,item_pedido_schema.tamanho,item_pedido_schema.preco_unit,id_pedido)
    
    session.add(item_pedido)    
    Pedido.calcular_preco()
    session.commit()
    return{
        "mensagem":"item criado com sucesso",
        "item_id":item_pedido.id,
        "preco_pedido":Pedido.preco
    }
    

       
#EXCLUIR um item
@order_router.post('/pedido/excluir_item/{id_item_pedido}') #path

async def excluir_item_pedido(id_item_pedido:int, session: Session = Depends(pegar_sessao), usuario:user = Depends(verificar_token)):
    
    #busco o item aonde os ids batem entre relação do pedido e do item
    item_pedido=session.query(Itempedido).filter(Itempedido.id==id_item_pedido).first()
    print(item_pedido)
    if not item_pedido:
        raise HTTPException(status_code=400,detail="pedido não enconctrado")
    
    #busca o pedido em si, --busco o pedido em si atravez do id do item no pedido
    Pedido_do_item=session.query(pedido).filter(pedido.id==item_pedido.pedido).first()
    #para olhar para o elemento em si, n o numero e tals

    
    if not usuario.admin and usuario.id != Pedido_do_item.usuario:
        raise HTTPException(status_code=401,detail="n tem autorização pra isso fi")
        
    session.delete(item_pedido)    
    Pedido_do_item.calcular_preco()
    session.commit()
    return{
        "mensagem":"item excluido com sucesso",
        "preco_pedido":item_pedido.preco
    }
    

