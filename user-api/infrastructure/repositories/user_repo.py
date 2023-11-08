"""
This module contains User concrete repository implementation
"""

from contextlib import AbstractContextManager
from typing import Callable, Type, TypedDict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists

from .base_repo import AsyncBaseRepository
from app.user.schemas.user import LoginResponseSchema
from core.db import Transactional
from core.exceptions import (
    PasswordDoesNotMatchException,
    DuplicateEmailOrNicknameException,
    UserNotFoundException,
)
from core.utils.token_helper import TokenHelper


class UserCriteria(TypedDict):
    """
    Custom type for user fields validation
    
    Args: 
        email (str): user email
    """
    email: str
    username: str


class UserRepository(AsyncBaseRepository):
    """
    Concrete implementation of User repository on
    infrastructure level. 
    """

    def __init__(self, model_cls: Type,
                 session_factory: Callable[..., AbstractContextManager[AsyncSession]]) -> None:
        super().__init__(model_cls, session_factory)

    async def check_user_exists(self, email: str, username: str) -> bool:
        """_summary_

        Args:
            email (str): _description_
            username (str): _description_

        Returns:
            bool: _description_
        """
        if self.async_exists(UserCriteria(email=email, username=username)):
            return True
        return False

    async def get_users_list(self) -> 