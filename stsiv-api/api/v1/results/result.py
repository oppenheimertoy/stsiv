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

from fastapi.responses import FileResponse

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
    test_result = await result_service.process_test_result(
        test_result_id=result_id
    )
    return test_result


@result_router.get("/{result_id}/getCustom")
async def get_custom_plot(
    result_id: UUID,
    current_user: CurrentUser = Depends(
        get_auth_user),
    result_service: TestResultService = Depends(
        BaseContainer().get_test_result_service
    )
) -> FileResponse:
    """_summary_

    Args:
        result_id (UUID): _description_
        current_user (CurrentUser, optional): _description_. Defaults to Depends( get_auth_user).
        result_service (TestResultService, optional): _description_. Defaults to Depends( BaseContainer().get_test_result_service ).

    Returns:
        FileResponse: _description_
    """
    pval_path = await result_service.get_custom_plot_dir(result_id)
    return FileResponse(pval_path)


@result_router.get("/{result_id}/getPval")
async def get_pval_plot(
    result_id: UUID,
    current_user: CurrentUser = Depends(
        get_auth_user),
    result_service: TestResultService = Depends(
        BaseContainer().get_test_result_service
    )
) -> FileResponse:
    """_summary_

    Args:
        result_id (UUID): _description_
        current_user (CurrentUser, optional): _description_. Defaults to Depends( get_auth_user).
        result_service (TestResultService, optional): _description_. Defaults to Depends( BaseContainer().get_test_result_service ).

    Returns:
        FileResponse: _description_
    """
    pval_path = await result_service.get_pvalue_plot_dir(result_id)
    return FileResponse(pval_path)

@result_router.get("/{result_id}/getStats")
async def get_text_result(
    result_id: UUID,
    current_user: CurrentUser = Depends(
        get_auth_user),
    result_service: TestResultService = Depends(
        BaseContainer().get_test_result_service
    )
) -> FileResponse:
    """_summary_

    Args:
        result_id (UUID): _description_
        current_user (CurrentUser, optional): _description_. Defaults to Depends( get_auth_user).
        result_service (TestResultService, optional): _description_. Defaults to Depends( BaseContainer().get_test_result_service ).

    Returns:
        FileResponse: _description_
    """
    result_path = await result_service.get_result_dir(result_id)
    return FileResponse(result_path)

@result_router.get("/{version_id}/list")
async def get_results_list(
    version_id: UUID,
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
        version_id
    )
    return [GetResultSchema(
        id=result[0].id,
        version_id=result[0].version_id,
        test_id=result[0].test_id,
        name=result[1]
    ) for result in results
    ]
