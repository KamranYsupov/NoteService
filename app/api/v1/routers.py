from fastapi import APIRouter

from app.core.config import settings
from .endpoints.user import router as user_router
from .endpoints.auth import router as auth_router

api_router = APIRouter()

# REST
api_router.include_router(user_router)
api_router.include_router(auth_router)

