"""
"""
from app.repositories import (
    UserRepository,
    ExperimentRepository,
    VersionRepository,
    TestRepository,
    TestResultRepository
)
from app.services import (
    UserService,
    ExperimentService,
    VersionService,
    TestService,
    TestResultService
)
from app.models import (
    Parameter,
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
    experiment_repository: ExperimentRepository = ExperimentRepository(
        async_db.session
    )
    version_repository: VersionRepository = VersionRepository(
        async_db.session
    )
    test_repository: TestRepository = TestRepository(
        async_db.session
    )
    test_result_repository: TestResultRepository = TestResultRepository(
        async_db.session
    )

    seeder: Seeder = Seeder([params_repository, test_repository])

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

    def get_version_service(self) -> VersionService:
        """_summary_

        Returns:
            VersionService: _description_
        """
        return VersionService(
            version_repo=self.version_repository,
            experiment_repo=self.experiment_repository
        )

    def get_test_service(self) -> TestService:
        """_summary_

        Returns:
            TestRepository: _description_
        """
        return TestService(
            test_repo=self.test_repository
        )

    def get_test_result_service(self) -> TestResultService:
        """_summary_

        Returns:
            TestResultService: _description_
        """
        return TestResultService(
            test_repo=self.test_repository,
            test_result_repo=self.test_result_repository
        )
