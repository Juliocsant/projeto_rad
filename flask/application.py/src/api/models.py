from tortoise import fields
from tortoise.models import Model

class UserModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    birth_date = fields.DateField()

    class Meta:
        table = "user"
