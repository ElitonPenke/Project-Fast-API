#no python em si n é preciso fixar o tipo de dados, porem é melhor dizer para melhor a velocidade e integridade

from pydantic import BaseModel
from typing import Optional

#essa classe vai me dizer o que eu preciso passar exatamente o formato do novo user
class UsuarioSchema(BaseModel):
    nome:str
    email:str
    senha:str
    ativo:Optional[bool]
    admin:Optional[bool]
    endereco:str
    
    #crio um subclass para linkar com o meu models do db(vai ser interpretado para tranformar para SQL)
    class Config:
        from_attributes=True
        
        
#essa classe vai me dizer o que eu preciso passar exatamente o formato de um novo pedido
class PedidoSchema(BaseModel):
    usuario:int   #armazena o id do usuario
    #status vem por padrão pendente
    #preco vem padrão, assim a unica infromação de preciso é o id do user
    
    class Config:
        from_attributes=True


class LoginSchema(BaseModel):
    email:str
    senha:str
    
    class Config:
        from_attributes=True
        
class ItemPedidoSchema(BaseModel):
    quantidade:int
    sabor:str
    tamanho:str
    preco_unit:float
    
    class Config:
        from_attributes=True
