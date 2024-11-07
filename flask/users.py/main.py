from fastapi import FastAPI, HTTPException, Depends
from pydantic import EmailStr
from passlib.context import CryptContext
from models import UserRegistration, UserLogin, UserUpdate, UserModel
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

app = FastAPI()

# Configuração do Tortoise ORM (DB Connection)
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",  # Aqui você pode usar o banco de dados desejado
    modules={"models": ["models"]},
    generate_schemas=True,  # Gere as tabelas automaticamente
    add_exception_handlers=True,
)

# Instância do passlib para criptografar senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para criptografar senha
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Função para verificar senha
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Rota para registrar um novo usuário
@app.post("/users/register")
async def register_user(user: UserRegistration):
    # Verifica se o e-mail já está em uso
    existing_user = await UserModel.get_or_none(email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

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
@app.post("/users/login")
async def login_user(user: UserLogin):
    # Verifica se o usuário existe
    db_user = await UserModel.get_or_none(email=user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Verifica se a senha está correta
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"message": "Login successful", "user": db_user.email}

# Rota para atualizar informações do usuário
@app.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    try:
        db_user = await UserModel.get(id=user_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    if user.name:
        db_user.name = user.name
    if user.email:
        db_user.email = user.email
    if user.password:
        db_user.password = hash_password(user.password)  # Criptografa a nova senha

    await db_user.save()

    return {"message": "User updated successfully", "user": db_user.email}
