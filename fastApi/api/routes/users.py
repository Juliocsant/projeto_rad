from fastapi import APIRouter
from fastApi.api.dtos.users import UserRegistration, UserLogin
from fastApi.datalayer.models.user import UserModel
from fastApi.api.exceptions.user import (login_wrong_excepetion,user_not_exist,email_already_exists)
from tortoise.exceptions import DoesNotExist, MultipleObjectsReturned
from fastapi import HTTPException
from fastApi.api.dtos.users import UserUpdate

router = APIRouter(
   prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register")
async def register(body: UserRegistration):

    email_exists = await UserModel.filter(email=body.email)
    if email_exists:
        raise email_already_exists()

    user = await UserModel.create(
        name = body.name,
        email = body.email,
        password = body.password,
        birth_date = body.birth_date,
    )
    return {'created': user}


@router.post("/login")
async def login(body: UserLogin):
    try:
        user = await UserModel.get(email=body.email)
    except DoesNotExist:
        raise user_not_exist()

    
    if user.password != body.password:
        raise login_wrong_excepetion()

    return user


@router.get("/get-users")
async def get_users():
    users = await UserModel.all()
    return {'users': users}



@router.put("/user_id")
async def update_user(user_id: int, body: UserUpdate):
    try:
        user = await UserModel.get(id=user_id)
        if body.name:
            user.name = body.name
        if body.email:
            user.email = body.email
        if body.password:
            user.password = body.password
        await user.save()
        return {"updated": user}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")



@router.delete("/user_id")
async def delete_user(user_id: int):
    try:
        user = await UserModel.get(id=user_id)
        await user.delete()
        return {"detail": "Usuário Deletado com sucesso"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")