"""
This module contains User concrete repository implementation
"""

from contextlib import AbstractContextManager
from typing import (
    Callable,
    Type,
    List,
    Awaitable
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from .base_repo import AsyncBaseRepository
from domain.entities.user import User
from dto.user import UserCriteria, UserDataDTO


class UserRepository(AsyncBaseRepository):
    """
    Concrete implementation of User repository on
    infrastructure level. 
    """

    def __init__(self,
                 session_factory: Callable[..., AbstractContextManager[AsyncSession]]) -> None:
        super().__init__(User, session_factory)

    async def check_user_exists(self, user_crit: UserCriteria) -> bool:
        """
        Check if user has already existed in database

        Args:
            user_crit (UserCriteria): 

        Returns:
            bool: True - if exisys, False overwise
        """
        if self.async_exists(**user_crit.to_dict()):
            return True
        return False

    async def get_users_list(self) -> List[Awaitable[User]]:
        """
        Get list of all entities in User model

        Returns:
            List[User]: all existing users
        """
        return self.async_list_elements()

    async def create_user(self, user_data: UserDataDTO) -> Awaitable[User]:
        """
        Create user

        Args:
            user_data (UserDataDTO): _description_

        Returns:
            Awaitable[User]: resulting user object
        """
        return self.async_create(**user_data.to_dict())

    async def get_user_by_email_or_username(self, token: str) -> Awaitable[User]:
        """
        Get user by given email or email

        Args:
            email (str): _description_

        Returns:
            Awaitable[User]: _description_
        """
        async with self.session_factory() as session:
            result = await session.execute(
                select(User).where(or_(User.email == token,
                                       User.username == token))
            )
            return result.scalars().first()
