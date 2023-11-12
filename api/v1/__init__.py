from fastapi import APIRouter

from api.v1.users.user import user_router
from api.v1.health.health import health_router

v1_router = APIRouter()
v1_router.include_router(user_router, prefix="/user")
v1_router.include_router(health_router, prefix="/health")
