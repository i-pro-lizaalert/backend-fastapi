from s3 import S3Client, S3File
from s3.core import RequestError
from app.exceptions import InternalServerError
from app.settings import S3_BUCKET,S3_SECRET_KEY,S3_ACCESS_KEY

def exception_wrapper(func):
    async def inner_func(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except RequestError as e:
            raise RequestError from e
        except Exception as e:
            raise InternalServerError(e) from e
    return inner_func

class S3:
    client: S3Client

    @classmethod
    async def connect_s3(cls) -> None:
        try:
            cls.client = S3Client(
                access_key=S3_ACCESS_KEY,
                secret_key=S3_SECRET_KEY,
                region='ru',
                s3_bucket=S3_BUCKET
            )
        except Exception as e:
            print(e)

    @classmethod
    @exception_wrapper
    async def list_file_names(cls, path) -> list[str]:
        if not cls.client:
            await S3.connect_s3()
        files = [f.key async for f in cls.client.list(path)]
        return files

    @classmethod
    @exception_wrapper
    async def list_files(cls, path) -> list[S3File]:
        if not cls.client:
            await S3.connect_s3()
        files = [f async for f in cls.client.list(path)]
        return files

    @classmethod
    @exception_wrapper
    async def delete_recursively(cls, path) -> None:
        if not cls.client:
            await S3.connect_s3()
        await cls.client.delete_recursive(path)

    @classmethod
    @exception_wrapper
    async def upload_file(cls, path, data) -> None:
        if not cls.client:
            await S3.connect_s3()
        await cls.client.upload(path,data)

    @classmethod
    @exception_wrapper
    async def download_file(cls, path):
        if not cls.client:
            await S3.connect_s3()
        return await cls.client.download(path)

    @classmethod
    async def disconnect_s3(cls) -> None:
        await cls.client.close()