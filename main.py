from fastapi import FastAPI

app= FastAPI()

#aqui importamos as rotas
from auth_routes import auth_router
from order_routes import order_router

#aqui importamos os rotiadores
app.include_router(auth_router)
app.include_router(order_router)