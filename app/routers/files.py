from datetime import timedelta

from fastapi import APIRouter, UploadFile, File, Form, Query
from pydantic import Field
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

import app.queries.users as users_queries
from app.models import UserOut
from app.auth.hash import get_password_hash, verify_password
from app.auth.jwt_token import create_access_token
from app.auth.oauth2 import get_current_user
from app.exceptions import ForbiddenException
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models import FileTags, SuccessfullResponse, Photo, PhotoOut, FileOut, Tag
from app.utils import format_record, format_records
from s3.core import RequestError
import app.queries.files as files_queries
from app.exceptions import BadRequest

files_router = APIRouter(tags=["Files"])

@files_router.post('/synchronize', response_model=SuccessfullResponse)
async def synchronize_s3() -> SuccessfullResponse:
    await files_queries.synchronize_files()
    return SuccessfullResponse()

@files_router.get('/file', response_model=FileOut)
async def get_file(path: str = Query('', title='Путь к файлу')) -> FileOut:
    try:
        photo, tags, fname = await files_queries.get_file(path)
    except RequestError as e:
        raise BadRequest('Неверный путь') from e
    photo = format_record(photo, PhotoOut)
    print(photo)
    tags = format_records(tags, Tag)
    result = FileOut(path=fname,tags=tags,photo=photo)
    return result

@files_router.get('/list', response_model=list[str])
async def get_file_names(path: str = Query('', title='Путь к директории')):
    try:
        result = await files_queries.get_file_names(path)
    except RequestError as e:
        raise BadRequest('Неверный путь') from e
    return result

# TODO: добавить удаление файлов
