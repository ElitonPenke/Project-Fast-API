from fastapi import APIRouter # roteador que vai fazer o modelo
from models import user,db #importar para fazer pesquisa no meu bd
from sqlalchemy.orm import sessionmaker # aqui faz uma seção para n ter paraleelismo de compretividade de requisições no meu bacno de dados

auth_router = APIRouter(prefix="/autenticacao", tags=['roteador_autenticacao']) #definindo que todas as rotas aqui vai ficar dentro de auth 
#ex: dominio/autenticacao/...

@auth_router.get("/")
async def home():
    return{"mensagem":"rota padrão de autenticação"}


#codigo aonde deu certo 200
#codgio aonde deu errado


#estou postando informações no meu bd
@auth_router.post("/criar_conta")
async def criar_conta(nome:str,email:str,senha:str,endereco=str): #passa os parametos e o proprio fastapi vai verificar os tipos da variavel
    
    Session=sessionmaker(bind=db)
    session=Session() # aqui eu abro uma seção, porem tenho que fechar ele
    
    usuario= session.query(user).filter(user.email==email).first() #uma query para ver se tem um user do bd igual ao meu atual tentando inserir
    
    if usuario:
        return {"ja existe um usuario com esse email"}
    else:
        novo_usuario= user(nome,email,senha,endereco)
        session.add(novo_usuario)
        session.commit() #comita tudo e encera a seção
        return {"Usuario cadastrado com sucesso meu chapa"}