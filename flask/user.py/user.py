from fastapi import HTTPException

def login_wrong_exception():
    """Lança uma exceção quando o e-mail ou senha estão incorretos"""
    raise HTTPException(status_code=404, detail="E-mail ou senha inválidos.")

def user_not_exist():
    """Lança uma exceção quando o usuário não existe"""
    raise HTTPException(status_code=404, detail="Usuário não existe.")

def email_already_exists():
    """Lança uma exceção quando o e-mail já está cadastrado"""
    raise HTTPException(status_code=409, detail="E-mail já cadastrado.")
