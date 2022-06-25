from uuid import UUID
from datetime import timedelta

from fastapi import APIRouter, UploadFile, File, Form, Query
from pydantic import Field
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordRequestForm

import app.queries.case as cases_queries
from app.models import UserOut
from app.auth.hash import get_password_hash, verify_password
from app.auth.jwt_token import create_access_token
from app.auth.oauth2 import get_current_user
from app.exceptions import ForbiddenException
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models import FileTags, SuccessfullResponse, Case, CaseIn, Photo, PhotoOut, CaseOut, UserOut2
from app.utils import format_record, format_records
import app.queries.files as files_queries

cases_router = APIRouter(tags=["Cases"])

@cases_router.post('/case', response_model=UUID)
async def update_case(case: Case) -> SuccessfullResponse:
    result = await cases_queries.update_case(case.id, case.name)
    return result

@cases_router.get('/case/all', response_model=list[CaseOut])
async def get_cases() -> list[CaseOut]:
    result = await cases_queries.get_cases()
    result = format_records(result, CaseOut)
    return result

@cases_router.get('/case/user/all', response_model=list[UserOut2])
async def get_case_users(id: UUID = Query(..., title='UUID кейса')):
    result = await cases_queries.get_case_users(id)
    result = format_records(result, UserOut2)
    return result

@cases_router.get('/user/case/all', response_model=list[CaseOut])
async def get_user_cases(username: str = Depends(get_current_user)) -> list[CaseOut]:
    result = await cases_queries.get_user_cases(username)
    result = format_records(result, CaseOut)
    return result

@cases_router.delete('/case', response_model=SuccessfullResponse)
async def delete_case(case: CaseIn) -> SuccessfullResponse:
    await cases_queries.delete_case(case.id)
    return SuccessfullResponse()

@cases_router.post('/user/case', response_model=SuccessfullResponse)
async def add_user_to_case(case: CaseIn, username: str = Depends(get_current_user)) -> SuccessfullResponse:
    await cases_queries.add_user_to_case(username, case.id)
    return SuccessfullResponse()

@cases_router.delete('/user/case', response_model=SuccessfullResponse)
async def remove_user_from_case(case: CaseIn, username: str = Depends(get_current_user)) -> SuccessfullResponse:
    await cases_queries.remove_from_case(username, case.id)
    return SuccessfullResponse()

@cases_router.post('/case/file', response_model=SuccessfullResponse)
async def case_add_files(photos: list[Photo], case: CaseIn, username: str = Depends(get_current_user)):
    await cases_queries.case_add_files(username,case.id,photos)
    return SuccessfullResponse()

@cases_router.delete('/case/file', response_model=SuccessfullResponse)
async def case_remove_files(photos: list[Photo], case: CaseIn, username: str = Depends(get_current_user)):
    await cases_queries.case_remove_files(username,case.id,photos)
    return SuccessfullResponse()

@cases_router.get('/case/file', response_model=list[str])
async def case_get_user_files(case_id: UUID = Query('', title='UUID кейса'), username: str = Depends(get_current_user)):
    result = await cases_queries.case_load_files(username,case_id)
    return result

