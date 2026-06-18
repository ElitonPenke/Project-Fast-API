from fastapi import APIRouter,Depends,HTTPException # roteador que vai fazer o modelo, o caminho para abri e fechar o banco e a questão de erros
from models import user
from dependecies import pegar_sessao

from schemas import UsuarioSchema # importo meu modleo de parametro para o meu banco de dado

#parte da criptgrafia
from main import bcrypt_context

from sqlalchemy.orm import Session


auth_router = APIRouter(prefix="/autenticacao", tags=['roteador_autenticacao']) #definindo que todas as rotas aqui vai ficar dentro de auth 
#ex: dominio/autenticacao/...

@auth_router.get("/")
async def home():
    return{"mensagem":"rota padrão de autenticação"}


#codigo aonde deu certo 200
#codgio aonde deu errado 400


#estou postando informações no meu bd
@auth_router.post("/criar_conta")                                #o user n passa esse parametro e sim ele puxa do Depends
async def criar_conta(user_Schema:UsuarioSchema,session = Depends(pegar_sessao)): #passa os parametos e o proprio fastapi vai verificar os tipos da variavel
    
    
    usuario= session.query(user).filter(user.email==user_Schema.email).first() #uma query para ver se tem um user do bd igual ao meu atual tentando inserir
    
    if usuario:
        #raise para interromper a função com erro
        raise HTTPException(status_code=400, detail="ja existe um usuario com esse email")
    else:
        senha_criptgrafada=bcrypt_context.hash(user_Schema.senha) #hash é para tranformar em codigo aleatorio minha string
        novo_usuario= user(user_Schema.nome,user_Schema.email,senha_criptgrafada,user_Schema.endereco,user_Schema.admin,user_Schema.admin)
        session.add(novo_usuario)
        session.commit() #comita tudo e encera a seção
        return {"mensagem": f"Usuario cadastrado com sucesso meu chapa, bem vindo {user_Schema.nome}"}