from uuid import UUID
from datetime import datetime
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

class Tag(BaseModel):
    name: str = Field(..., title='Имя тега')

class Photo(BaseModel):
    path: str = Field(..., title='Путь к файлу')

class PhotoOut(BaseModel):
    source: str = Field(None, title='Путь к файлу на S3')
    description: str = Field(None, title='Описание фотографии')
    date: datetime = Field(None, title='Дата обновления')


class FileTags(BaseModel):
    file: Photo
    tags: list[Tag]

class FileOut(BaseModel):
    photo: PhotoOut
    tags: list[Tag]
    path: str = Field(None, title='Путь к фотографии для фронтенда')

class Case(BaseModel):
    id: UUID = Field(None, title='ID кейса')
    name: str = Field(..., title='Имя кейса')

class CaseOut(BaseModel):
    id: UUID = Field(None, title='ID кейса')
    name: str = Field(..., title='Имя кейса')
    participated: int = Field(None, title='Количество участников')
    photos: int = Field(None, title='Количество фоток')

class CaseIn(BaseModel):
    id: UUID = Field(..., title='ID кейса')