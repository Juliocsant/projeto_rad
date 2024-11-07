from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model
from tortoise import fields

# Definindo o modelo do banco de dados para as postagens
class PostModel(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()  # ID do usuário que fez a postagem
    content = fields.TextField()  # Conteúdo da postagem
    created_at = fields.DatetimeField(auto_now_add=True)  # Data de criação da postagem
    updated_at = fields.DatetimeField(auto_now=True)  # Data de atualização da postagem

    class Meta:
        table = "post"

# Recebe dados da postagem
class PostRequest(BaseModel):
    user_id: int
    content: str

# Esquemas de resposta
Post_Pydantic = pydantic_model_creator(PostModel, name="Post")
PostIn_Pydantic = pydantic_model_creator(PostModel, name="PostIn", exclude_readonly=True)
