from pydantic import BaseModel, EmailStr
from tortoise import fields
from tortoise.models import Model

# Modelo de dados do usuário (Tortoise ORM)
class UserModel(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    birth_date = fields.DateField()

    class Meta:
        table = "user"

# Esquemas Pydantic para os dados de entrada
class UserRegistration(BaseModel):
    name: str
    email: EmailStr
    password: str
    birth_date: str  # Se preferir, pode usar Date para validar datas corretamente

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
