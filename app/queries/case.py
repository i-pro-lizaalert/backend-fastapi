import os
import hashlib
from uuid import UUID
from asyncio import gather
from asyncpg import Record
from app.services.db import DB
from app.services.s3 import S3
from app.queries.files import get_file
from asyncpg.exceptions import UniqueViolationError
from app.exceptions import BadRequest, NotFoundException

async def update_case(id: UUID, name: str) -> None:
    sql = """
        insert into cases (id, name)
        values (coalesce($1, id), name)
        on conflict (id) do update 
        set name = excluded.name
    """
    await DB.execute(sql, id, name)

async def get_cases() -> list[Record]:
    sql = """
        select id, name from cases
    """
    return await DB.fetch(sql)

async def get_user_cases(username: str) -> list[Record]:
    sql = """
        select id, name from cases as c 
        join users_cases uc on c.id = uc.case_id
        join users as u on uc.user_id = u.id
        where u.username = $1
    """
    return await DB.fetch(sql, username)

async def delete_case(id: UUID) -> None:
    sql = """
        delete from cases
        where id = $1
    """
    await DB.execute(sql, id)

async def remove_from_case(username: str, id: UUID) -> None:
    sql = """
        select id from users
        where username = $1
    """
    user_id = await DB.fetchval(sql, username)
    sql = """
        delete from users_cases
        where user_id = $1 and case_id = $2
    """
    await DB.execute(sql, user_id, id)


async def check_user_case(username: str, id: UUID) -> int:
    sql = """
            select uc.user_id from users_cases as uc
            join users u on uc.user_id = u.id
            where u.username = $1 and uc.case_id = $2
        """
    user_id = await DB.fetchval(sql, username, id)
    if not user_id:
        raise NotFoundException('Пользователь не учавствует в кейсе')
    return user_id

async def check_file(path: str) -> None:
    sql = """
        select source from files
        where source = $1
    """
    result = await DB.fetchval(sql)
    if not result:
        raise NotFoundException('Файл не найден')

async def case_add_files(username: str, case_id: UUID, path_names: list[str]) -> None:
    def add_file(path: str, case_id):
        await check_file(path)
        sql = """
            insert into files_cases(file_id, case_id) 
            values($1, $2)
        """
        try:
            await DB.execute(sql,path,case_id)
        except UniqueViolationError:
            raise BadRequest('Файл уже добавлен')

    await check_user_case(username, case_id)
    coroutines = [add_file(path, case_id) for path in path_names]
    await gather(*coroutines)

async def case_remove_files(username: str, case_id: UUID, path_names: list[str]) -> None:
    def remove_file(path: str, case_id):
        await check_file(path)
        sql = """
            delete from files_cases
            where file_id = $1 and case_id = $2
        """
        try:
            await DB.execute(sql,path,case_id)
        except UniqueViolationError:
            raise BadRequest('Файл уже добавлен')

    await check_user_case(username, case_id)
    coroutines = [remove_file(path, case_id) for path in path_names]
    await gather(*coroutines)

async def case_load_files(username: str, case_id: UUID) -> list[(Record, list[Record], str)]:
    await check_user_case(username, case_id)
    sql = """
        select file_id from files_cases
        where case_id = $1
    """
    path_names = await DB.fetch(sql, case_id)
    coroutines = [get_file(path['file_id']) for path in path_names]
    return list(await gather(*coroutines))


