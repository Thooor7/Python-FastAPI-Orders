# Projeto Python FastAPI

Este projeto é um exemplo simples de API construída com FastAPI e Alembic para controle de migrações de banco de dados. Todos os dados são fictícios e usados apenas para aprendizado.

## Estrutura do projeto

- `main.py` - ponto de entrada da aplicação FastAPI
- `auth_routes.py` - rotas de autenticação e login
- `orders_routes.py` - rotas de pedidos
- `models.py` - definição dos modelos SQLAlchemy
- `alembic/` - diretório de migrações do Alembic
- `alembic.ini` - configuração do Alembic
- `banco.db` - banco SQLite local (não deve ser versionado)

## Requisitos

- Python 3.11+
- FastAPI
- SQLAlchemy
- Alembic

## Instalação

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

> Se você não tiver `requirements.txt`, instale manualmente `fastapi`, `uvicorn`, `sqlalchemy`, `alembic` e `python-dotenv`.

## Executando o projeto

```bash
uvicorn main:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`.

## Migrações com Alembic

- Inicializar Alembic (já feito neste projeto):
  ```bash
  alembic init alembic
  ```
- Criar nova revisão com autogeracao:
  ```bash
  alembic revision --autogenerate -m "Migracao inicial"
  ```
- Aplicar migrações:
  ```bash
  alembic upgrade head
  ```

## Observações

Este projeto é destinado a estudo e pequenas provas de conceito..