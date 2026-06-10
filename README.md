# 🍕 API de Gestão de Pedidos - FastAPI

Um projeto de API REST desenvolvido com **FastAPI** para gerenciar autenticação de usuários e pedidos. Este é um projeto educacional baseado no curso de FastAPI da [Hashtag Programação](https://www.youtube.com/@HashtagProgramacao).

---

## 📋 Sobre o Projeto

Esta API fornece funcionalidades básicas para:
- ✅ Autenticação e cadastro de usuários
- ✅ Gestão de pedidos
- ✅ Controle de itens de pedidos com informações de sabor, tamanho e preço

**Status**: 🚀 Em desenvolvimento (Fase de aprendizado)

---

## 🏗️ Arquitetura do Projeto

```
.
├── main.py                 # Arquivo principal da aplicação FastAPI
├── models.py              # Modelos SQLAlchemy (Tabelas do BD)
├── auth_routes.py         # Rotas de autenticação
├── order_routes.py        # Rotas de pedidos
├── banco_De_dados.db      # Banco de dados SQLite
└── README.md              # Este arquivo
```

---

## 📦 Estrutura do Banco de Dados

### Tabela: `usuarios`
```sql
- id (Integer, Primary Key)
- nome (String, obrigatório)
- email (String, obrigatório, único)
- senha (String, obrigatório)
- endereco (String, obrigatório)
- ativo (Boolean, padrão: True)
- admin (Boolean, padrão: False)
```

### Tabela: `pedidos`
```sql
- id (Integer, Primary Key)
- usuario (Foreign Key → usuarios.id)
- status (String, padrão: "PENDENTE")
- preco (Float)
```

**Status possíveis**: `PENDENTE`, `CANCELADO`, `FINALIZADO`

### Tabela: `itens_pedidos`
```sql
- id (Integer, Primary Key)
- pedido (Foreign Key → pedidos.id)
- quantidade (Integer)
- sabor (String)
- tamanho (String)
- preco_unit (Float)
```


## 📚 Recursos de Aprendizado

- 📖 [Documentação Oficial FastAPI](https://fastapi.tiangolo.com/)
- 🎬 [Curso Hashtag Programação](https://www.youtube.com/@HashtagProgramacao)
- 🔐 [Passlib - Hash de Senhas](https://passlib.readthedocs.io/)
- 🛡️ [JWT para FastAPI](https://fastapi.tiangolo.com/tutorial/security/first-steps/)
- ✅ [Pydantic - Validação](https://docs.pydantic.dev/)
