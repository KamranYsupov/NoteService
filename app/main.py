from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from loguru import logger

from app.core.config import settings
from app.core.container import Container, container
from app.api.v1 import routers
from app.db import Base, db_manager
from app.core.logger import log_exception


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):

    yield

    await db_manager.dispose()


def create_app() -> FastAPI:
    fastapi_app = FastAPI(
        title=settings.project_name,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    fastapi_app.container = container
    fastapi_app.include_router(routers.api_router, prefix=settings.api_v1_prefix)



    return fastapi_app


app = create_app()

@app.middleware('http')
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.info(f'{request.method} {request.url} - {response.status_code}')
    return response


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    log_exception(exc)
    return ORJSONResponse(
        status_code=500,
        content={'message': 'Произошла ошибка на сервере.'},
    )
    
    
if __name__ == '__main__':
    uvicorn.run(app='app.main:app', reload=True)
