"""
"""
from typing import List
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
)

from app.services import ExperimentService
from app.schemas import (
    CreateExperimentRequest,
    GetExperimentSchema
)

from core.containers.base_container import BaseContainer
from core.dependencies.auth import AuthenticationRequired
from core.dependencies.current_user import (
    get_auth_user
)
from core.middleware.schemas.current_user import CurrentUser


experiment_router = APIRouter()


@experiment_router.get("/list", dependencies=[Depends(AuthenticationRequired)])
async def get_user_experiments(
    current_user: CurrentUser = Depends(get_auth_user),
    experiment_service: ExperimentService = Depends(
        BaseContainer().get_experiment_service)
) -> List[GetExperimentSchema]:
    """_summary_

    Args:
        current_user (CurrentUser, optional): _description_. Defaults to Depends(get_auth_user).
        experiment_service (ExperimentService, optional): _description_. 
        Defaults to Depends(BaseContainer().get_experiment_service).

    Returns:
        List[GetExperimentSchema]: _description_
    """
    return await experiment_service.get_user_experiments(current_user.id)


@experiment_router.get("/{experiment_id}/info", dependencies=[Depends(AuthenticationRequired)])
async def get_experiment_info(
    experiment_id : UUID,
    current_user: CurrentUser = Depends(get_auth_user),
    experiment_service: ExperimentService = Depends(
        BaseContainer().get_experiment_service)
) -> GetExperimentSchema:
    """_summary_

    Args:
        experiment_id (UUID): _description_
        current_user (CurrentUser, optional): _description_. Defaults to Depends(get_auth_user).
        experiment_service (ExperimentService, optional): _description_. Defaults to Depends( BaseContainer().get_experiment_service).

    Returns:
        GetExperimentSchema: _description_
    """
    return await experiment_service.get_experiment(
        experiment_id=experiment_id
    )


@experiment_router.post("/create", dependencies=[Depends(AuthenticationRequired)])
async def create_experiment(
    experiment_data: CreateExperimentRequest,
    current_user: CurrentUser = Depends(get_auth_user),
    experiment_service: ExperimentService = Depends(
        BaseContainer().get_experiment_service)
) -> GetExperimentSchema:
    """_summary_

    Args:
        experiment_data (CreateExperimentRequest): _description_
        current_user (CurrentUser, optional): _description_. Defaults to Depends(get_auth_user).

    Returns:
        GetExperimentSchema: _description_
    """
    return await experiment_service.create_experiment(creator_id=current_user.id,
                                                      name=experiment_data.name,
                                                      description=experiment_data.description)
