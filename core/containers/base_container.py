"""
"""
from app.repositories import (
    UserRepository,
    ExperimentRepository
)
from app.services import (
    UserService,
    ExperimentService
)
from app.models import (
    Parameter,
    Test,
)

from core.database.database import AsyncEngineController
from core.config import config
from core.repository.base_repo import AsyncBaseRepository
from core.database.seeder import Seeder


class BaseContainer:
    """
    This is the factory container that will instantiate all the controllers and
    repositories which can be accessed by the rest of the application.
    """

    async_db: AsyncEngineController = AsyncEngineController(
        str(config.SQLALCHEMY_ASYNC_DATABASE_URI))
    # Repositories
    user_repository: UserRepository = UserRepository(async_db.session)
    params_repository: AsyncBaseRepository = AsyncBaseRepository(
        Parameter, async_db.session)
    tests_repository: AsyncBaseRepository = AsyncBaseRepository(
        Test, async_db.session)
    experiment_repository: ExperimentRepository = ExperimentRepository(
        async_db.session
    )

    seeder: Seeder = Seeder([params_repository, tests_repository])

    def get_user_service(self) -> UserService:
        """_summary_

        Returns:
            _type_: _description_
        """
        return UserService(
            user_repo=self.user_repository
        )

    def get_experiment_service(self) -> ExperimentService:
        """_summary_

        Returns:
            ExperimentService: _description_
        """
        return ExperimentService(
            experiment_repo=self.experiment_repository
        )
