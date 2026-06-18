#no python em si n é preciso fixar o tipo de dados, porem é melhor dizer para melhor a velocidade e integridade

from pydantic import BaseModel
from typing import Optional

#essa classe vai me dizer o que eu preciso passar exatamente o formato
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