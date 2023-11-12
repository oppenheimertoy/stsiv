from typing import Callable
from contextlib import (
    AbstractContextManager
)

from sqlalchemy.ext.asyncio import (
    AsyncSession
)

from fastapi import Depends

# from app.controllers import AuthController, TaskController, UserController
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService
from core.database.database import AsyncEngineController
from core.config import config


class BaseContainer:
    """
    This is the factory container that will instantiate all the controllers and
    repositories which can be accessed by the rest of the application.
    """

    async_db: AsyncEngineController = AsyncEngineController(
        str(config.SQLALCHEMY_ASYNC_DATABASE_URI))
    # Repositories
    user_repository = UserRepository(async_db.session)

    def get_user_service(self) -> UserService:
        """_summary_

        Returns:
            _type_: _description_
        """
        return UserService(
            user_repo=self.user_repository
        )
