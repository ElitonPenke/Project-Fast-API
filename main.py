#liga o servidor FastAPI ---uvicorn main:app --reload

from passlib.context import CryptContext #criptografar as senhas
from fastapi import FastAPI
from dotenv import load_dotenv


#parte de criptografia
import os
load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")

bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")  #o deprecated para usar sempre schemas validos



app= FastAPI()

#aqui importamos as rotas
from auth_routes import auth_router
from order_routes import order_router

#aqui importamos os rotiadores
app.include_router(auth_router)
app.include_router(order_router)

