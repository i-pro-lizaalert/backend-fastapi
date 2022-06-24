from fastapi import Form
from pydantic import BaseModel, Field
from typing import Optional

class SuccessfullResponse(BaseModel):
    details: str = Field('Выполнено', title='Статус операции')

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    login: Optional[str] = None

class UserIn(BaseModel):
    name: str = Form(..., title='Имя пользователя')
    surname: str = Form(..., title='Фамилия пользователя')

class UserOut(UserIn):
    username: str = Field(..., title='Логин аккаунта')
    avatar: str = Field(None, title='Аватар аккаунта')

