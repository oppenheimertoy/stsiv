"""
"""
from uuid import UUID
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File
)

from app.services import (
    VersionService,
    TestResultService,
)
from app.schemas import (
    GetVersionSchema,
    CreateVersionRequest,
    ListVersionRequest,
    VersionParamsRequest
)

from core.containers.base_container import BaseContainer
from core.dependencies.auth import AuthenticationRequired
from core.dependencies.current_user import (
    get_auth_user
)
from core.middleware.schemas.current_user import CurrentUser


version_router = APIRouter()


@version_router.get("/list", dependencies=[Depends(AuthenticationRequired)])
async def get_experiment_versions(
    list_versions: ListVersionRequest,
    current_user: CurrentUser = Depends(get_auth_user),
    version_service: VersionService = Depends(
        BaseContainer().get_version_service
    )
) -> List[GetVersionSchema]:
    """_summary_

    Args:
        current_user (CurrentUser, optional): _description_. Defaults to Depends(get_auth_user).
        version_service (VersionService, optional): _description_. Defaults to Depends( BaseContainer().get_version_service ).

    Returns:
        List[GetVersionSchema]: _description_
    """
    return await version_service.get_experiment_versions(experiment_id=list_versions.experiment_id)


@version_router.post("/create", dependencies=[Depends(AuthenticationRequired)])
async def create_experiment(
    version_data: CreateVersionRequest,
    current_user: CurrentUser = Depends(get_auth_user),
    version_service: VersionService = Depends(
        BaseContainer().get_version_service)
) -> GetVersionSchema:
    """_summary_

    Args:
        experiment_data (CreateExperimentRequest): _description_
        current_user (CurrentUser, optional): _description_. Defaults to Depends(get_auth_user).

    Returns:
        GetExperimentSchema: _description_
    """
    return await version_service.create_version(experiment_id=version_data.experiment_id,
                                                name=version_data.name,
                                                description=version_data.description)


@version_router.post("/{version_id}/upload")
async def upload_file_for_version(
    version_id: UUID,
    file: UploadFile = File(...),
    current_user: CurrentUser = Depends(
        get_auth_user),
    is_data_file: bool = True,
    version_service: VersionService = Depends(
        BaseContainer().get_version_service)
):
    """_summary_

    Args:
        version_id (UUID): _description_
        file (UploadFile, optional): _description_. Defaults to File(...).
        current_user (CurrentUser, optional): _description_. Defaults to Depends( get_auth_user).
        is_data_file (bool, optional): _description_. Defaults to True.
        version_service (VersionService, optional): _description_. 
        Defaults to Depends( BaseContainer().get_version_service).

    Returns:
        _type_: _description_
    """
    file_path = await version_service.upload_version_file(version_id, file, is_data_file)
    return {"file_path": file_path}


@version_router.put("/{version_id}/params")
async def update_versions_params(
    version_id: UUID,
    params: VersionParamsRequest,
    current_user: CurrentUser = Depends(
        get_auth_user),
    test_result_service: TestResultService = Depends(
        BaseContainer().get_test_result_service),
    version_service: VersionService = Depends(
        BaseContainer().get_version_service)
) -> GetVersionSchema:
    """_summary_

    Args:
        version_id (UUID): _description_
        params (VersionParamsRequest): _description_

    Returns:
        GetVersionSchema: _description_
    """
    updated_version = await version_service.update_version_params(
        version_id=version_id,
        new_params=params
    )
    await test_result_service.create_result(
        version_id=version_id,
        test_identifiers=params.tests.value
    )
    return updated_version


@version_router.post("/{version_id}/run")
async def run_tests(
    version_id: UUID,
    current_user: CurrentUser = Depends(
        get_auth_user),
    version_service: VersionService = Depends(
        BaseContainer().get_version_service)
):
    """_summary_

    Args:
        version_id (UUID): _description_
        current_user (CurrentUser, optional): _description_. Defaults to Depends( get_auth_user).
        version_service (VersionService, optional): _description_. 
        Defaults to Depends( BaseContainer().get_version_service).

    Returns:
        str: _description_
    """
    return {"command": await version_service.calculate_version(version_id=version_id)}
