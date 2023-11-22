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
    GetResultSchema,
    ListResultsRequest
)

from core.containers.base_container import BaseContainer
from core.dependencies.auth import AuthenticationRequired
from core.dependencies.current_user import (
    get_auth_user
)
from core.middleware.schemas.current_user import CurrentUser


result_router = APIRouter()


@result_router.post("/{result_id}/getResult")
async def get_test_result(
    result_id: UUID,
    current_user: CurrentUser = Depends(
        get_auth_user),
    result_service: TestResultService = Depends(
        BaseContainer().get_test_result_service
    )
):
    """_summary_

    Args:
        result_id (UUID): _description_
        current_user (CurrentUser, optional): _description_. Defaults to Depends( get_auth_user).
        result_service (TestResultService, optional): _description_. Defaults to Depends( BaseContainer().get_test_result_service ).
    """
    path = await result_service.process_test_result(
        test_result_id=result_id
    )
    return str(path)


@result_router.get("/list")
async def get_results_list(
    list_res_data: ListResultsRequest,
    current_user: CurrentUser = Depends(
        get_auth_user),
    result_service: TestResultService = Depends(
        BaseContainer().get_test_result_service
    )
) -> List[GetResultSchema]:
    """_summary_

    Args:
        version_id (UUID): _description_
        list_res_data (ListResultsRequest): _description_
        current_user (CurrentUser, optional): _description_. 
        Defaults to Depends( get_auth_user).
        result_service (TestResultService, optional): _description_. 
        Defaults to Depends( BaseContainer().get_test_result_service ).

    Returns:
        List[GetResultSchema]: _description_
    """
    results = await result_service.list_results(
        list_res_data.version_id
    )
    return [GetResultSchema.model_validate(
            result, from_attributes=True) for result in results
            ]
