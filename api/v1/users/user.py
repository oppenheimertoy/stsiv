from typing import List

from fastapi import APIRouter, Depends, Request, Response

from app.services.user_service import UserService
# from app.models.user import User
from app.schemas.jwt import TokenSchema
from app.schemas.request.user import LoginUserRequest, RegisterUserRequest
from app.schemas.response.user import UserResponse
from app.models.user import User
from core.containers.base_container import BaseContainer
from core.dependencies.auth import AuthenticationRequired
from core.dependencies.current_user import get_current_user
from core.middleware.auth_middleware import AuthBackend

user_router = APIRouter()


@user_router.get("/list", dependencies=[Depends(AuthenticationRequired)])
async def get_users(
    request: Request,
    user_service: UserService = Depends(BaseContainer().get_user_service)
) -> List[UserResponse]:
    """_summary_

    Args:
        user_service (UserController, optional): _description_. 
        Defaults to Depends(Factory().get_user_controller).

    Returns:
        list[UserResponse]: _description_
    """
    authenticated, current_user = await AuthBackend().authenticate(request)
    if not authenticated:
        return Response("Unauthorized", status_code=401)
    users = await user_service.get_user_list()
    users_list = [UserResponse.model_validate(user,
                                              from_attributes=True) for user in users]
    return users_list


@user_router.post("/sign-up", status_code=201)
async def register_user(
    register_user_request: RegisterUserRequest,
    user_service: UserService = Depends(BaseContainer().get_user_service)
) -> UserResponse:
    """_summary_

    Args:
        register_user_request (RegisterUserRequest): _description_
        user_service (UserService, optional): _description_. Defaults to Depends(BaseContainer().get_user_service).

    Returns:
        UserResponse: _description_
    """
    new_user = await user_service.create_user(
        email=register_user_request.email,
        password1=register_user_request.password1,
        password2=register_user_request.password2,
        username=register_user_request.username,
        name=register_user_request.name,
        surname=register_user_request.surname
    )

    return UserResponse(id=new_user.id,
                        email=new_user.email,
                        username=new_user.username)


@user_router.post("/sign-in")
async def login_user(
    login_user_request: LoginUserRequest,
    user_service: UserService = Depends(BaseContainer().get_user_service)
) -> TokenSchema:
    """_summary_

    Args:
        login_user_request (LoginUserRequest): _description_
        user_service (UserService, optional): _description_. Defaults to Depends(BaseContainer().get_user_service).

    Returns:
        TokenSchema: _description_
    """
    return await user_service.login(
        token=login_user_request.token, password=login_user_request.password
    )


@user_router.get("/me", dependencies=[Depends(AuthenticationRequired)])
def get_user(
    user: User = Depends(get_current_user),
) -> UserResponse:
    return UserResponse(id=user.id,
                        email=user.email,
                        username=user.username)
