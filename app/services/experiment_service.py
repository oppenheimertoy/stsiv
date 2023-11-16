"""
"""
from typing import (
    List,
    Awaitable
)

from uuid import UUID

from app.models.experiment import Experiment
from app.schemas.jwt import TokenSchema
from app.repositories.experiment_repo import ExperimentRepository
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


class ExperimentService:
    """_summary_
    """
    def __init__(self, experiment_repo: ExperimentRepository):
        self.experiment_repo = experiment_repo
        
    async def create_experiment(self, creator_id: UUID,
                                name: str, description: str) -> Awaitable[Experiment]:
        """_summary_

        Args:
            creator_id (UUID): _description_
            name (str): _description_
            description (str): _description_

        Returns:
            Awaitable[Experiment]: _description_
        """
        