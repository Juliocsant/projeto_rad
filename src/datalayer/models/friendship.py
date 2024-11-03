from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class FriendshipModel(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.UserModel", related_name="friends", on_delete=fields.CASCADE)
    friend = fields.ForeignKeyField("models.UserModel", related_name="friend_of", on_delete=fields.CASCADE)
    status = fields.CharField(max_length=20, default="active")  
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user", "friend"),)

Friendship_Pydantic = pydantic_model_creator(FriendshipModel, name="Friendship")
FriendshipIn_Pydantic = pydantic_model_creator(FriendshipModel, name="FriendshipIn", exclude_readonly=True)