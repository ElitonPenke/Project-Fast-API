#cd c:\users\elito\project_fast_api
#.venv\Scripts\activate   
#deactivate
#liga o servidor FastAPI uvicorn main:app --reload

import bcrypt #criptografar as senhas
from fastapi import FastAPI
from dotenv import load_dotenv


#parte de criptografia
import os
load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")



app= FastAPI()

#aqui importamos as rotas
from auth_routes import auth_router
from order_routes import order_router

#aqui importamos os rotiadores
app.include_router(auth_router)
app.include_router(order_router)

