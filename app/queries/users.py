import hashlib
from fastapi import UploadFile, File
from asyncpg import Record
from asyncpg.exceptions import UniqueViolationError, PostgresError
from app.services.db import DB
from app.exceptions import BadRequest, NotFoundException, InternalServerError


async def add_user(name: str, surname: str, username: str, hashed_password: str, file: UploadFile) -> None:
    fname = None
    if file:
        data = file.file.read()
        fname = f'static/{hashlib.sha224(data).hexdigest()}.png'
        with open(fname, mode='wb+') as f:
            f.write(data)
    sql = """  INSERT INTO users(name, surname, username, hashed_password, avatar)
               VALUES ($1,$2,$3,$4,$5)
               ON CONFLICT(username) DO UPDATE
               SET name = excluded.name, surname = excluded.surname,
               hashed_password = excluded.hashed_password, avatar = excluded.avatar"""
    await DB.execute(sql, name,surname, username, hashed_password, fname)


async def get_user_by_username(username: str) -> Record:
    sql = """ SELECT id,name,surname,username,hashed_password,avatar
              FROM users
              WHERE username = $1"""
    result = await DB.fetchrow(sql,username)
    if not result:
        raise NotFoundException('Пользователь не найден')
    return result


