from sqlalchemy.orm import sessionmaker # aqui faz uma seção para n ter paraleelismo de compretividade de requisições no meu banco de dados
from models import db #importar para fazer pesquisa no meu bd


#ao inves de colocar para abrie e fechar um sessao em cada lugar do codigo aonde tem rotas ao meu banco e dados, vamos fazer uma def para reutlizar em todo o codigo

def pegar_sessao():
    
    try:
        Session=sessionmaker(bind=db)
        session=Session() # aqui eu abro uma seção, porem tenho que fechar ele
        yield session #retorna um valor, porem n encerra a def
    
    finally: #para que independete se deu certo,errado, ele fecha a session para n sobrecarregar o banco e dados
        session.close()