from fastapi import APIRouter
from src.api.dtos.users import UserRegistration, UserLogin
from src.datalayer.models.user import UserModel
from src.api.exceptions.user import (login_wrong_excepetion,user_not_exist,email_already_exists)
from tortoise.exceptions import DoesNotExist, MultipleObjectsReturned

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

