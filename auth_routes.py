from fastapi import APIRouter,Depends,HTTPException # roteador que vai fazer o modelo, o caminho para abri e fechar o banco e a questão de 
from fastapi.security import OAuth2PasswordRequestForm # insatncia dos dados do formulario
from models import user
from dependecies import pegar_sessao,verificar_token

from schemas import UsuarioSchema # importo meu modleo de parametro para o meu banco de dado
from schemas import LoginSchema
#parte da criptgrafia
from main import bcrypt,ACCESS_TOKEN_EXPERIUS_MINUTES,ALG,SECRET_KEY

import jwt

from sqlalchemy.orm import Session
from datetime import datetime,timedelta,timezone


#sempre que quiser pegar alguma infromação do banco para verificar e tals, sempre usar o session.query("tabela").filter("tabela".coluna == ....)

auth_router = APIRouter(prefix="/autenticacao", tags=['roteador_autenticacao']) #definindo que todas as rotas aqui vai ficar dentro de auth 
#ex: dominio/autenticacao/...

#jwt (json web token)
def criar_token(id_usuario,duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPERIUS_MINUTES)):
    data_experacao=datetime.now(timezone.utc) + duracao_token
    
    dic_info={"sub":str(id_usuario),"exp":data_experacao}
    
    jwt_cript=jwt.encode(dic_info,SECRET_KEY,ALG)
    
    return jwt_cript

def autenticar_usuario(email,senha,session):
    usuario = session.query(user).filter(user.email==email).first()
    
    if not usuario:
        return False
    elif not bcrypt.checkpw(senha.encode('utf-8'),usuario.senha.encode('utf-8')):
        return False
    return usuario

@auth_router.get("/")
async def home():
    return{"mensagem":"rota padrão de autenticação"}


#codigo aonde deu certo 200
#codgio aonde deu errado 400


#estou postando informações no meu bd
@auth_router.post("/criar_conta")                          #o user n passa esse parametro e sim ele puxa do Depends
async def criar_conta(user_Schema:UsuarioSchema,session = Depends(pegar_sessao)): #passa os parametos e o proprio fastapi vai verificar os tipos da variavel
    
    #print(user_Schema.model_dump())
    
    usuario= session.query(user).filter(user.email==user_Schema.email).first() #uma query para ver se tem um user do bd igual ao meu atual tentando inserir
    
    
    if usuario:
        #raise para interromper a função com erro
        raise HTTPException(status_code=400, detail="ja existe um usuario com esse email")
    else:
        
        #aqui o bcrypt converte para bytes, criptografa, converte para texteo normal  e o gensalt ele cria um texteo aletaotio para cda senha em si 
        senha_criptgrafada=bcrypt.hashpw(user_Schema.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') #hash é para tranformar em codigo aleatorio minha string
        novo_usuario= user(user_Schema.nome,user_Schema.email,senha_criptgrafada,user_Schema.endereco,user_Schema.admin,user_Schema.admin)
        session.add(novo_usuario)
        session.commit() #comita tudo e encera a seção
        return {"mensagem": f"Usuario cadastrado com sucesso meu chapa, bem vindo {user_Schema.nome}"}
    
    
#login ->email e senha - > token JWT
@auth_router.post("/login")
async def login(login_schema:LoginSchema,session: Session = Depends(pegar_sessao)):
    
    usuario = autenticar_usuario(login_schema.email, login_schema.senha,session)
    
    if not usuario:
        raise HTTPException(status_code=400, detail="user ñ encontrado ou senha incorreta")
    else:
        #cria um token para o user
        access_token = criar_token(usuario.id)
        refresh_token=criar_token(usuario.id,duracao_token=timedelta(days=15))
        return {
            'access_token':access_token,
            'refresh_token':refresh_token,
            'token_type': "Bearer"
                }

#utilizar o token refresh, verifica a entrada token verificado e atualiza
@auth_router.get("/refresh")
async def use_refresh_token(usuario:user = Depends(verificar_token)):
    
    access_token=criar_token(user.id)
    return {
            'access_token':access_token,
            'token_type': "Bearer"
            }
    
    
#--------------------------------------------------------------------------------------
#para testar na documentação o login por meio no oauth2 
@auth_router.post("/login_pelo_form")
async def login_pelo_form(dados_formulario:OAuth2PasswordRequestForm=Depends() ,session: Session = Depends(pegar_sessao)):
    
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password,session)
    
    if not usuario:
        raise HTTPException(status_code=400, detail="user ñ encontrado ou senha incorreta")
    else:
        #cria um token para o user
        access_token = criar_token(usuario.id)

        return {
            'access_token':access_token,
            'token_type': "Bearer"
                }
