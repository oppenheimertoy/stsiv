from uuid import UUID

from fastapi import (
    Depends,
    Request,
    HTTPException,
    status
)
from app.services.user_service import UserService
from core.containers.base_container import BaseContainer
from core.middleware.auth_middleware import AuthBackend
from core.middleware.schemas.current_user import CurrentUser


async def get_current_user(
    request: Request,
    user_service: UserService = Depends(BaseContainer().get_user_service),
):
    """_summary_

    Args:
        request (Request): _description_
        user_service (UserService, optional): _description_. Defaults to Depends(BaseContainer().get_user_service).

    Returns:
        _type_: _description_
    """
    return await user_service.get_user_by_id(request.user.id)


async def get_auth_user(request: Request) -> CurrentUser:
    """_summary_

    Args:
        request (Request): _description_

    Raises:
        HTTPException: _description_

    Returns:
        CurrentUser: _description_
    """
    authenticated, current_user = await AuthBackend().authenticate(request)
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return CurrentUser(id=current_user.id)
