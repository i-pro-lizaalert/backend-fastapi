from datetime import timedelta

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

import app.queries.users as users_queries
from app.models import SuccessfullResponse, UserIn, UserOut
from app.auth.hash import get_password_hash, verify_password
from app.auth.jwt_token import create_access_token
from app.auth.oauth2 import get_current_user
from app.exceptions import NotFoundException, BadRequest, ForbiddenException
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils import format_record

users_router = APIRouter(tags=["Users"])


@users_router.post('/registration')
async def registration_user(name: str = Form(..., title='Имя пользователя'), surname: str = Form(..., title='Фамилия пользователя'), avatar: UploadFile = File(None, title='Аватар аккаунта'), request: OAuth2PasswordRequestForm = Depends()) -> dict:
    request.password = get_password_hash(request.password)
    await users_queries.add_user(name, surname, request.username, request.password, avatar)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": request.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@users_router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends()) -> dict:
    print(request.username)
    user = await users_queries.get_user_by_username(request.username)
    if not verify_password(request.password, user['hashed_password']):
        raise ForbiddenException('Неверный пароль')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": request.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@users_router.get('/user', response_model=UserOut)
async def get_user_name(login: str = Depends(get_current_user)) -> str:
    user = await users_queries.get_user_by_username(login)
    user = format_record(user, UserOut)
    return user