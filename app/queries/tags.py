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

from asyncpg import Record
from asyncpg.exceptions import UniqueViolationError, PostgresError
from app.services.db import DB
from app.models import Tag
from app.exceptions import BadRequest, NotFoundException, InternalServerError


async def add_tags_file(tags: list[Tag], path: str) -> None:
    sql = """
        insert into tags(name)
        values($1) 
        on conflict(name) do nothing 
    """
    coroutines = [DB.fetchval(sql, tag.name) for tag in tags]
    await gather(*coroutines)
    sql = """
        select id from tags
        where name = ANY($1::text[])
    """
    ids = await DB.fetch(sql, [tag.name for tag in tags])
    sql = """
        insert into files_tags(file_id, tag_id)
        values ($1, $2) on conflict do nothing 
    """
    coroutines = [DB.execute(sql, path,id['id']) for id in ids]
    await gather(*coroutines)

async def remove_tags_from_file(tags: list[Tag], path: str) -> None:
    sql = """
        select id from tags
        where name = ANY($1::text[])
    """
    ids = await DB.fetch(sql,[tag.name for tag in tags])
    sql = """
        delete from files_tags
        where file_id = $1 and tag_id = ANY($2::text[])
    """
    await DB.execute(sql, path, tags)

async def search_tags(tags: list[str]) -> list[str]:
    sql = """
        select id from tags
        where name = ANY($1::text[])    
    """
    ids = await DB.fetch(sql, tags)
    sql = """
        WITH ids AS
        (SELECT ft.file_id,count(tag_id)
          FROM files_tags AS ft
          WHERE ft.tag_id = ANY($1::int[])
          GROUP BY ft.file_id)
        SELECT f.source
        FROM files AS f
        JOIN ids ON f.source = ids.file_id
        WHERE ids.count = $2
    """
    return [file['source'] for file in await DB.fetch(sql, ids, len(ids))]
