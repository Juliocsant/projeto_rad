from pydantic import BaseModel

class UserRegistration(BaseModel):
    name: str
    email: str
    password: str