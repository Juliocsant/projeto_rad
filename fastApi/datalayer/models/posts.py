from tortoise.models import Model
from tortoise import fields

class PostModel(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.UserModel", related_name="posts")
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "post"