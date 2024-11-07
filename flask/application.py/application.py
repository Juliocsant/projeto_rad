from fastapi import FastAPI
from src.api.configuration import configure_db, configure_routes

def create_app():
    app = FastAPI()

    # Configura as rotas da aplicação
    configure_routes(app)

    # Configura o banco de dados
    configure_db(app)
   
    return app

# Instanciando a aplicação FastAPI
app = create_app()

@app.get('/')
async def home():
    return {'status': 'ok'}
