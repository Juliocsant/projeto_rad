from fastapi import APIRouter, HTTPException
from fastApi.api.dtos.posts import PostRequest  
from fastApi.api.dtos.friendship import FriendshipRequest  
from fastApi.datalayer.models.posts import PostModel
from fastApi.datalayer.models.friendship import FriendshipModel
from tortoise.exceptions import DoesNotExist

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def create_post(body: PostRequest):
    post = await PostModel.create(
        user_id=body.user_id,
        content=body.content,
    )
    return {'created': post}

@router.get("/")
async def get_posts():
    posts = await PostModel.all()
    return {'posts': posts}

@router.get("/{post_id}")
async def get_post(post_id: int):
    try:
        post = await PostModel.get(id=post_id)
        return post
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Postagem não encontrada")

@router.put("/{post_id}")
async def update_post(post_id: int, body: PostRequest):
    try:
        post = await PostModel.get(id=post_id)
        post.content = body.content
        await post.save()
        return {"updated": post}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Postagem não encontrada")

@router.delete("/{post_id}")
async def delete_post(post_id: int):
    try:
        post = await PostModel.get(id=post_id)
        await post.delete()
        return {"detail": "Postagem deletada com sucesso"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Postagem não encontrada")


# Rotas para Amizades
friendship_router = APIRouter(
    prefix="/friendships",
    tags=["friendships"],
    responses={404: {"description": "Not found"}},
)

@friendship_router.post("/")
async def create_friendship(body: FriendshipRequest):
    friendship = await FriendshipModel.create(
        user_id=body.user_id,
        friend_id=body.friend_id,
    )
    return {'created': friendship}

@friendship_router.get("/")
async def get_friendships():
    friendships = await FriendshipModel.all()
    return {'friendships': friendships}

@friendship_router.delete("/{friendship_id}")
async def delete_friendship(friendship_id: int):
    try:
        friendship = await FriendshipModel.get(id=friendship_id)
        await friendship.delete()
        return {"detail": "Amizade deletada com sucesso"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Amizade não encontrada")