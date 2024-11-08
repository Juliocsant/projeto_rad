from pydantic import BaseModel

class UserRegistration(BaseModel):
    name: str
    email: str
    password: str
    birth_date: str


class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None    