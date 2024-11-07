from fastapi import APIRouter

router = APIRouter()

# Exemplo de rota de amizade (esta é apenas uma estrutura inicial)
@router.post("/create")
async def create_friendship(user_id_1: int, user_id_2: int):
    # A lógica de criar uma amizade entre dois usuários
    return {"message": "Friendship created", "user_1": user_id_1, "user_2": user_id_2}
