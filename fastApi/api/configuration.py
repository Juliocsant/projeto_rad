from fastapi import FastAPI 
from tortoise.contrib.fastapi import register_tortoise
from fastApi.api.routes import users, friendship, posts

def configure_routes(app: FastAPI):
    app.include_router(users.router)
    app.include_router(friendship.router)
    app.include_router(posts.router)  
    
def configure_db(app: FastAPI):
    register_tortoise(
        app=app,
        config={
            'connections': {
                # 'default': 'postgres://postgres:qwerty123@localhost:5432/events'
                'default': 'sqlite://db.sqlite3'
            },
            'apps': {
                'models': {
                    'models': [
                        'fastApi.datalayer.models.user',
                        'fastApi.datalayer.models.friendship'  
                    ],
                    'default_connection': 'default',
                }
            }
        },


        generate_schemas=True,
        add_exception_handlers=True,  
    )
