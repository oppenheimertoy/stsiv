from fastapi import Depends, Request

from app.services.user_service import UserService
from core.containers.base_container import BaseContainer


async def get_current_user(
    request: Request,
    user_controller: UserService = Depends(BaseContainer().get_user_service),
):
    return await user_controller.get_by_id(request.user.id)
