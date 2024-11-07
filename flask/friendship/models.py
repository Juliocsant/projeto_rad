from tortoise import fields
from tortoise.models import Model

class FriendshipModel(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    friend_id = fields.IntField()

    class Meta:
        table = "friendships"
