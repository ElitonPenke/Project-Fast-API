from sqlalchemy.orm import sessionmaker
from models import Itempedido, db,user,pedido #importar para fazer pesquisa no meu bd

Session=sessionmaker(bind=db)
session=Session()


'''#deletar somente um
session.query(user).filter(user.admin != True).delete()
session.commit()
session.close()'''


session.query(Itempedido).delete()
session.commit()
session.close()