from datetime import timedelta

from fastapi import APIRouter, UploadFile, File, Form, Query
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

import app.queries.users as users_queries
from app.models import UserOut
from app.auth.hash import get_password_hash, verify_password
from app.auth.jwt_token import create_access_token
from app.auth.oauth2 import get_current_user
from app.exceptions import ForbiddenException
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models import FileTags, SuccessfullResponse, Tag
from app.utils import format_record
import app.queries.tags as tags_queries

tags_router = APIRouter(tags=["Tags"])


@tags_router.post('/file/tags', response_model=SuccessfullResponse)
async def add_tags_to_file(tags: FileTags) -> SuccessfullResponse:
    await tags_queries.add_tags_file(tags.tags, tags.file.path)
    return SuccessfullResponse()

@tags_router.delete("/file/tags", response_model=SuccessfullResponse)
async def login(tags: FileTags) -> SuccessfullResponse:
    await tags_queries.add_tags_file(tags.tags, tags.file.path)
    return SuccessfullResponse()

@tags_router.get('/file/search', response_model=list[str])
async def search_tags(tags: list[str] = Query(..., title='Список тегов')) -> list[str]:
    return await tags_queries.search_tags(tags)
