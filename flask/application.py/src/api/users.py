from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from src.api.models import UserModel
from user import login_wrong_exception, user_not_exist, email_already_exists

# Cria o roteador para as rotas de usuários
user_router = APIRouter()

# Instância do passlib para criptografar senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para criptografar senha
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Função para verificar senha
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

class UserRegistration(BaseModel):
    name: str
    email: EmailStr
    password: str
    birth_date: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None

# Rota para registrar um novo usuário
@user_router.post("/register")
async def register_user(user: UserRegistration):
    # Verifica se o e-mail já está em uso
    existing_user = await UserModel.get_or_none(email=user.email)
    if existing_user:
        email_already_exists()  # Utiliza a função de exceção personalizada

    # Criptografa a senha
    hashed_password = hash_password(user.password)

    # Cria o usuário no banco de dados
    new_user = await UserModel.create(
        name=user.name,
        email=user.email,
        password=hashed_password,
        birth_date=user.birth_date,
    )

    return {"message": "User created successfully", "user": new_user.email}

# Rota para login de usuário
@user_router.post("/login")
async def login_user(user: UserLogin):
    # Verifica se o usuário existe
    db_user = await UserModel.get_or_none(email=user.email)
    if not db_user:
        user_not_exist()  # Utiliza a função de exceção personalizada

    # Verifica se a senha está correta
    if not verify_password(user.password, db_user.password):
        login_wrong_exception()  # Utiliza a função de exceção personalizada

    return {"message": "Login successful", "user": db_user.email}

# Rota para atualizar informações do usuário
@user_router.put("/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    try:
        db_user = await UserModel.get(id=user_id)
    except DoesNotExist:
        user_not_exist()  # Utiliza a função de exceção personalizada

    if user.name:
        db_user.name = user.name
    if user.email:
        db_user.email = user.email
    if user.password:
        db_user.password = hash_password(user.password)  # Criptografa a nova senha

    await db_user.save()

    return {"message": "User updated successfully", "user": db_user.email}
