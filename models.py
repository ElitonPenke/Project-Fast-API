#aqui vamos fazer um banco de dados local para testar

from sqlalchemy import create_engine,Column,String,Integer,Boolean,Float,ForeignKey  #ele que cria em si o bd
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

#so trocar o "" par ao db certo 
db=create_engine("sqlite:///banco_De_dados.db") #cria coneção

base=declarative_base() #cria a base do banco

#cria as tabelas do banco

#user
class user (base):
    __tablename__="usuarios"
    
    #nome de como eu acesso no meu codigo / nome como vai aparecer no meu banco de dados
    
    id=Column("id",Integer,primary_key=True,autoincrement=True)
    nome=Column("nome",String,nullable=False)
    email=Column("email",String,nullable=False)
    senha=Column("senha",String,nullable=False)
    ativo=Column("ativo",Boolean,default=True)
    admin=Column("admin",Boolean,default=False)
    endereco=Column("endereco",String,nullable=False)

    def __init__ (self,nome,email,senha,endereco,ativo=True,admin=False):    #a função que vai rodar quando colocar um novo usuario
        self.nome=nome
        self.email=email
        self.senha=senha
        self.ativo=ativo
        self.admin=admin
        self.endereco=endereco
        
#pedido
class pedido(base):
    __tablename__="pedidos"
    
    '''   ("PENDENTE","PENDENTE"),
        ("CANCELADO","CANCELADO"),
        ("FINALIZADO","FINALIZADO")
    )
    '''

    id=Column("id",Integer,primary_key=True,autoincrement=True)
    status=Column("status",String)
    usuario=Column("usuario",ForeignKey(user.id))
    preco=Column("preco",Float)
    
    def __init__(self,usuario,status="PENDENTE",preco=0):
        self.usuario=usuario
        self.status=status
        self.preco=preco
    
#itens_do_pedido
class Itempedido(base):
    __tablename__="itens_pedidos"
    
    id=Column("id",Integer,primary_key=True,autoincrement=True)
    quantidade=Column("quantidade",Integer)
    sabor=Column("sabor",String)
    tamanho=Column("tamanho",String)
    preco_unit=Column("preco_unit",Float)
    pedido=Column("pedido",ForeignKey("pedidos.id"))
    
    def __init__(self,quantidade,sabor,tamanho,preco_unit,pedido):
        self.quantidade=quantidade
        self.sabor=sabor
        self.tamanho=tamanho
        self.preco_unit=preco_unit
        self.pedido=pedido
