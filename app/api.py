# import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
#
from app.services.db import DB
from app.services.s3 import S3
from app.exceptions import CommonException, InternalServerError
from app.routers.users import users_router

origins = ["*"] # TODO: change it in bright future
app = FastAPI(title='I-PRO Backend')
# logger = logging.getLogger(__name__)
#
@app.on_event('startup')
async def startup() -> None:
    await DB.connect_db()
    await S3.connect_s3()
    await S3.list_file_names('')

@app.on_event('shutdown')
async def shutdown() -> None:
    await DB.disconnect_db()
    await S3.disconnect_s3()

@app.exception_handler(CommonException)
async def common_exception_handler(request: Request, exception: CommonException) -> JSONResponse:
    # logger.error(exception.error)
    if isinstance(exception, InternalServerError):
        return JSONResponse(
            status_code=exception.code,
            content={'details': 'Internal Server Error'}
        )
    return JSONResponse(
        status_code=exception.code,
        content={'detatils': exception.error}
    )
app.include_router(users_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.mount('/static', StaticFiles(directory='static'), name='static')