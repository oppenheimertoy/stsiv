"""
"""
from typing import (
    List,
    Awaitable
)

from uuid import UUID

from app.models.user import User
from app.schemas.jwt import TokenSchema
from app.repositories.user_repo import UserRepository
from app.dto.user import UserCriteria, UserDataDTO

from core.exceptions.user import (
    DuplicateEmailOrNicknameException,
    PasswordDoesNotMatchException,
    UserNotFoundException,
    IncorrectPasswordException,
)
from core.secure.pass_security import PasswordHandler
from core.exceptions.base import UnauthorizedException
from core.utils.token_helper import TokenHelper


class UserService:
    """_summary_
    """

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_user_list(
        self
    ) -> List[Awaitable[User]]:
        """_summary_

        Returns:
            List[Awaitable[User]]: _description_
        """
        return await self.user_repo.get_users_list()

    async def create_user(
            self, email: str, password1: str, password2: str, username: str,
            name: str, surname: str) -> Awaitable[User]:
        """_summary_

        Args:
            email (str): _description_
            password1 (str): _description_
            password2 (str): _description_
            username (str): _description_
            name (str): _description_
            surname (str): _description_

        Raises:
            PasswordDoesNotMatchException: _description_
            DuplicateEmailOrNicknameException: _description_
        """
        if password1 != password2:
            raise PasswordDoesNotMatchException

        encr_pass = PasswordHandler().hash(password1)

        if await self.user_repo.check_user_exists(UserCriteria(email=email,
                                                               username=username)):
            raise DuplicateEmailOrNicknameException

        return await self.user_repo.create_user(UserDataDTO(username=username, email=email,
                                                            _password=encr_pass, name=name,
                                                            surname=surname))

    async def login(self, token: str, password: str) -> TokenSchema:
        """_summary_

        Args:
            token (str): _description_
            password (str): _description_

        Raises:
            UserNotFoundException: _description_
            IncorrectPasswordException: _description_

        Returns:
            LoginResponseSchema: _description_
        """
        user: User = await self.user_repo.get_user_by_email_or_username(token=token)
        if not user:
            raise UserNotFoundException

        if PasswordHandler().verify(user.password, password) is False:
            raise IncorrectPasswordException

        response = TokenSchema(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(
                payload={"sub": "refresh_token"},
                expire_period=72000),
        )
        return response

    async def refresh_token(self, access_token: str, refresh_token: str) -> TokenSchema:
        """_summary_

        Args:
            access_token (str): _description_
            refresh_token (str): _description_

        Raises:
            UnauthorizedException: _description_

        Returns:
            TokenSchema: _description_
        """
        token = TokenHelper.decode_expired_token(access_token)
        refresh_token = TokenHelper.decode(refresh_token)
        if refresh_token.get("sub") != "refresh_token":
            raise UnauthorizedException("Invalid refresh token")

        return TokenSchema(
            token=TokenHelper.encode(
                payload={"user_id": token.get("user_id")}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh_token"})
        )

    async def get_user_by_id(self, id_: UUID) -> Awaitable[User]:
        """_summary_

        Args:
            id_ (UUID): _description_

        Returns:
            Awaitable[User]: _description_
        """
        return await self.user_repo.async_get(id_)
