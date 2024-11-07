from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from src.api.users import user_router

def configure_db(app: FastAPI):
    """
    Configura o banco de dados (Tortoise ORM) e as migrações.
    """
    register_tortoise(
        app,
        db_url="sqlite://db.sqlite3",  # Altere conforme o banco de dados
        modules={"models": ["src.api.models"]},
        generate_schemas=True,  # Gere as tabelas automaticamente
        add_exception_handlers=True,
    )

def configure_routes(app: FastAPI):
    """
    Registra as rotas da aplicação.
    """
    app.include_router(user_router, prefix="/users", tags=["users"])
