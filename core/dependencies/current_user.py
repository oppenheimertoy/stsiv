from fastapi import Depends, Request

from app.services.user_service import UserService
from core.containers.base_container import BaseContainer


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
