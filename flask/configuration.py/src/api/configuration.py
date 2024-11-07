from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from src.api.routes import users, friendship, posts

def configure_routes(app: FastAPI):
    # Inclui os routers para cada entidade
    app.include_router(users.router)
    app.include_router(friendship.router)
    app.include_router(posts.router)  

def configure_db(app: FastAPI):
    # Configuração do banco de dados (Tortoise ORM)
    register_tortoise(
        app=app,
        config={
            'connections': {
                'default': 'sqlite://db.sqlite3',  # Usando SQLite como banco de dados
            },
            'apps': {
                'models': {
                    'models': [
                        'src.datalayer.models.user',        # Importa os modelos de usuários
                        'src.datalayer.models.friendship',  # Importa os modelos de amizade
                        'src.datalayer.models.post',        # Importa os modelos de postagens
                    ],
                    'default_connection': 'default',
                }
            }
        },
        generate_schemas=True,  # Gera as tabelas automaticamente
        add_exception_handlers=True,  # Adiciona os manipuladores de exceções padrão do Tortoise
    )
    