from fastapi import APIRouter, HTTPException
from src.datalayer.models.friendship import FriendshipModel
from src.datalayer.models.user import UserModel
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import DoesNotExist


User_Pydantic = pydantic_model_creator(UserModel, name="User")

router = APIRouter(
    prefix="/friendships",
    tags=["friendships"],
)

@router.post("/add")
async def add_friend(user_id: int, friend_id: int):
    if user_id == friend_id:
        raise HTTPException(status_code=400, detail="Você não pode ser seu próprio amigo.")
    
    friendship_exists = await FriendshipModel.filter(user_id=user_id, friend_id=friend_id).exists()
    if friendship_exists:
        raise HTTPException(status_code=400, detail="Amizade já existe.")
    
    await FriendshipModel.create(user_id=user_id, friend_id=friend_id, status="active")
    await FriendshipModel.create(user_id=friend_id, friend_id=user_id, status="active")
    
    return {"message": "Amigo adicionado."}

@router.delete("/remove")
async def remove_friend(user_id: int, friend_id: int):
    deleted_count = await FriendshipModel.filter(user_id=user_id, friend_id=friend_id).delete()
    deleted_count += await FriendshipModel.filter(user_id=friend_id, friend_id=user_id).delete()
    
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Amizade nao encontrada.")
    
    return {"message": "Amigo removido com sucesso."}

@router.put("/block")
async def block_friend(user_id: int, friend_id: int):
    updated_count = await FriendshipModel.filter(user_id=user_id, friend_id=friend_id).update(status="blocked")
    updated_count += await FriendshipModel.filter(user_id=friend_id, friend_id=user_id).update(status="blocked")
    
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Amizade não encontrada.")
    
    return {"message": "Amigo bloqueado com sucesso."}


@router.get("/list")
async def list_friends(user_id: int):
    friends = await FriendshipModel.filter(user_id=user_id, status="active").prefetch_related("friend")
    return {"friends": [await User_Pydantic.from_tortoise_orm(f.friend) for f in friends]}

@router.put("/unblock")
async def unblock_friend(user_id: int, friend_id: int):
    updated_count = await FriendshipModel.filter(user_id=user_id, friend_id=friend_id, status="blocked").update(status="active")
    updated_count += await FriendshipModel.filter(user_id=friend_id, friend_id=user_id, status="blocked").update(status="active")

    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Amigo não encontrado ou não bloqueado.")

    return {"message": "Amigo desbloqueado com sucesso."}