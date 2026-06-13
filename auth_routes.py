from fastapi import APIRouter,Depends # roteador que vai fazer o modelo
from models import user
from dependecies import pegar_sessao

#parte da criptgrafia
from main import bcrypt_context


auth_router = APIRouter(prefix="/autenticacao", tags=['roteador_autenticacao']) #definindo que todas as rotas aqui vai ficar dentro de auth 
#ex: dominio/autenticacao/...

@auth_router.get("/")
async def home():
    return{"mensagem":"rota padrão de autenticação"}


#codigo aonde deu certo 200
#codgio aonde deu errado 500


#estou postando informações no meu bd
@auth_router.post("/criar_conta")                                #o user n passa esse parametro e sim ele puxa do Depends
async def criar_conta(nome:str,email:str,senha:str,endereco=str,session = Depends(pegar_sessao)): #passa os parametos e o proprio fastapi vai verificar os tipos da variavel
    
    
    usuario= session.query(user).filter(user.email==email).first() #uma query para ver se tem um user do bd igual ao meu atual tentando inserir
    
    if usuario:
        return {"ja existe um usuario com esse email"}
    else:
        senha_criptgrafada=bcrypt_context.hash(senha) #hash é para tranformar em codigo aleatorio minha string
        novo_usuario= user(nome,email,senha_criptgrafada,endereco)
        session.add(novo_usuario)
        session.commit() #comita tudo e encera a seção
        return {"Usuario cadastrado com sucesso meu chapa"}