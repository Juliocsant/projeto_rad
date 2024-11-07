from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from tortoise.exceptions import DoesNotExist
from models import PostRequest, Post_Pydantic, PostIn_Pydantic, PostModel

app = FastAPI()

# Configuração do Tortoise ORM (DB Connection)
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",  # Aqui você pode usar o banco de dados desejado
    modules={"models": ["models"]},
    generate_schemas=True,  # Gere as tabelas automaticamente
    add_exception_handlers=True,
)

@app.post("/posts/", response_model=Post_Pydantic)
async def create_post(post_request: PostRequest):
    """
    Cria uma nova postagem no banco de dados.
    """
    post = await PostModel.create(**post_request.dict())
    return await Post_Pydantic.from_tortoise_orm(post)

@app.get("/posts/{post_id}", response_model=Post_Pydantic)
async def get_post(post_id: int):
    """
    Retorna os dados de uma postagem específica.
    """
    try:
        post = await PostModel.get(id=post_id)
        return await Post_Pydantic.from_tortoise_orm(post)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

@app.get("/posts/", response_model=list[Post_Pydantic])
async def list_posts():
    """
    Retorna todas as postagens.
    """
    posts = await PostModel.all()
    return await Post_Pydantic.from_queryset(posts)

@app.put("/posts/{post_id}", response_model=Post_Pydantic)
async def update_post(post_id: int, post_request: PostIn_Pydantic):
    """
    Atualiza uma postagem existente.
    """
    try:
        post = await PostModel.get(id=post_id)
        post.content = post_request.content
        post.user_id = post_request.user_id
        await post.save()
        return await Post_Pydantic.from_tortoise_orm(post)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

@app.delete("/posts/{post_id}", response_model=Post_Pydantic)
async def delete_post(post_id: int):
    """
    Exclui uma postagem.
    """
    try:
        post = await PostModel.get(id=post_id)
        await post.delete()
        return await Post_Pydantic.from_tortoise_orm(post)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")
