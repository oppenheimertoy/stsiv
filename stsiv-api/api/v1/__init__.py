from fastapi import APIRouter

from api.v1.users.user import user_router
from api.v1.health.health import health_router
from api.v1.experiments.experiment import experiment_router
from api.v1.versions.version import version_router
from api.v1.results.result import result_router

v1_router = APIRouter()
v1_router.include_router(user_router, prefix="/user")
v1_router.include_router(health_router, prefix="/health")
v1_router.include_router(experiment_router, prefix="/experiment")
v1_router.include_router(version_router, prefix="/version")
v1_router.include_router(result_router, prefix="/result")
