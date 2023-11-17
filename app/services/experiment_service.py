"""
"""
from typing import (
    List,
)

from uuid import UUID

from app.schemas.response.experiment import GetExperimentSchema
from app.repositories.experiment_repo import ExperimentRepository
from app.dto.experiment import ExperimentDataDTO


class ExperimentService:
    """_summary_
    """

    def __init__(self, experiment_repo: ExperimentRepository):
        self.experiment_repo = experiment_repo

    async def create_experiment(self, creator_id: UUID,
                                name: str, description: str) -> GetExperimentSchema:
        """_summary_

        Args:
            creator_id (UUID): _description_
            name (str): _description_
            description (str): _description_

        Returns:
            Awaitable[Experiment]: _description_
        """
        new_experiment = await self.experiment_repo.create_experiment(ExperimentDataDTO(
                                                                      creator_id=creator_id,
                                                                      name=name,
                                                                      description=description))
        return GetExperimentSchema(id=new_experiment.id,
                                   creator_id=new_experiment.creator_id,
                                   name=new_experiment.name,
                                   description=new_experiment.description,
                                   versions_num=new_experiment.versions_num)

    async def get_user_experiments(self, user_id: UUID) -> List[GetExperimentSchema]:
        """_summary_

        Args:
            user_id (UUID): _description_

        Returns:
            List[GetExperimentSchema]: _description_
        """
        user_experiments = await self.experiment_repo.get_experiment_list_by_user(
            creator_id=user_id)

        return [GetExperimentSchema.model_validate(
            experiment, from_attributes=True) for experiment in user_experiments]
