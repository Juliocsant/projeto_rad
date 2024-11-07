from flask import Flask, request, jsonify
from friendship import FriendshipRequest, Friendship_Pydantic, FriendshipIn_Pydantic
from tortoise import Tortoise
from models import FriendshipModel
import asyncio

app = Flask(__name__)

# Conexão com o banco de dados
async def init_db():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',  # Exemplo de banco de dados SQLite
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()

@app.before_first_request
def before_first_request():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())

@app.route('/friendship', methods=['POST'])
async def create_friendship():
    try:
        # Receber dados da requisição
        data = request.get_json()
        friendship_request = FriendshipRequest(**data)

        # Criar uma nova amizade
        friendship = await FriendshipModel.create(
            user_id=friendship_request.user_id,
            friend_id=friendship_request.friend_id
        )

        # Retornar a resposta no formato Pydantic
        friendship_pydantic = await Friendship_Pydantic.from_tortoise_orm(friendship)
        return jsonify(friendship_pydantic.dict())

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/friendship', methods=['GET'])
async def get_friendships():
    friendships = await FriendshipModel.all()
    friendships_pydantic = await Friendship_Pydantic.from_queryset(friendships)
    return jsonify([f.dict() for f in friendships_pydantic])


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
