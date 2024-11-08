from pydantic import BaseModel
from fastapi import HTTPException

def login_wrong_excepetion():

    raise HTTPException(status_code=404, detail="E-mail ou senha inválidos.")





def user_not_exist():
    raise HTTPException(status_code=404, detail="Usuário não existe.")


def email_already_exists():
    raise HTTPException(status_code=409, detail="E-mail ja cadastrado.")