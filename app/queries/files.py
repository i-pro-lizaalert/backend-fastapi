from asyncio import gather
import hashlib
from asyncpg import Record
from s3 import S3File
from fastapi import UploadFile, File
from app.exceptions import NotFoundException, BadRequest
from app.services.db import DB
from app.services.s3 import S3

# TODO: get_file jj/ ломает

async def get_file_names(path: str) -> list[str]:
    return await S3.list_file_names(path)

async def add_file(dir_path: str, file: UploadFile) -> None:
    data = file.file.read()
    datatype = file.file.name.split('.')[-1]
    fname = f'{hashlib.sha224(data).hexdigest()}.{datatype}'
    await S3.upload_file(dir_path+'/'+fname,data)

async def delete_file(path: str) -> None:
    await S3.delete_recursively(path)

# TODO: change this lazy synchronization
async def synchronize_files() -> None:
    async def add_file(path: S3File):
        sql = """
            insert into files(source, description, date)
            values ($1, null, $2)
        """
        await DB.execute(sql, path.key, path.last_modified.replace(tzinfo=None))
    sql = """
        truncate table files cascade
    """
    await DB.execute(sql)
    paths = await S3.list_files('')
    coroutines = [add_file(path) for path in paths]
    await gather(*coroutines)

async def get_file(path: str) -> (Record, list[Record],str):
    sql = """
        select source, description, date from files
        where source = $1
    """
    file = await DB.fetchrow(sql,path)
    if not file:
        raise NotFoundException('Файл не найден')
    data = await S3.download_file(path)
    datatype = path.split('.')[-1]
    fname = f'{hashlib.sha224(data).hexdigest()}.{datatype}'
    with open(f'static/{fname}', mode='wb+') as f:
        f.write(data)
    sql = """
        select t.name from tags as t
        join files_tags as ft
        on ft.tag_id = t.id
        where ft.file_id = $1
    """
    tags = await DB.fetch(sql, path)
    print(file,tags,fname)
    return file,tags,f'static/{fname}'