"""_summary_
"""
from uuid import UUID
from fastapi import UploadFile
from typing import (
    List
)

from pathlib import Path
import aiofiles

from app.dto import VersionDataDTO
from app.repositories import VersionRepository, ExperimentRepository
from app.schemas import (
    GetVersionSchema,
    VersionParamsRequest
)
from app.services.argument_parser.args_parser_extended import STSConfig
from app.services.subprocess_service.subprocess_controller import STSProcessController


class VersionService:
    """_summary_
    """

    def __init__(
        self,
        version_repo: VersionRepository,
        experiment_repo: ExperimentRepository
    ):
        self.experiment_repo: ExperimentRepository = experiment_repo
        self.version_repo: VersionRepository = version_repo

        self.base_result_dir = Path(
            __file__).resolve().parent.parent.parent / 'result'

    async def create_version(self, experiment_id: UUID,
                             name: str, description: str) -> GetVersionSchema:
        """_summary_

        Args:
            experiment_id (UUID): _description_
            name (str): _description_
            description (str): _description_

        Returns:
            GetVersionSchema: _description_
        """
        if name is None:
            name = self.generate_version_name()
        return await self.version_repo.create_version(VersionDataDTO(experiment_id=experiment_id,
                                                                     name=name,
                                                                     description=description))

    async def get_version_info(
        self,
        version_id: UUID
    ) -> GetVersionSchema:
        """_summary_

        Args:
            version_id (UUID): _description_

        Returns:
            GetVersionSchema: _description_
        """
        version = await self.version_repo.async_get(
            id_=version_id
        )
        return GetVersionSchema.model_validate(
            version, from_attributes=True)

    async def get_experiment_versions(self, experiment_id: UUID) -> List[GetVersionSchema]:
        """_summary_

        Args:
            experiment_id (UUID): _description_

        Returns:
            List[GetVersionSchema]: _description_
        """
        experiment_versions = await self.version_repo.get_version_list_by_experiment(
            experiment_id=experiment_id)

        return [GetVersionSchema.model_validate(
            version, from_attributes=True) for version in experiment_versions
        ]

    async def generate_version_name(self) -> str:
        """_summary_

        Returns:
            _type_: _description_
        """
        version_count = await self.version_repo.count_versions()
        return f"Version_{version_count + 1}"

    async def set_status(self, version_id: UUID, new_status: str):
        """_summary_

        Args:
            version_id (_type_): _description_
            new_status (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Call the async_update method with the version ID and new status
        return await self.version_repo.async_update(version_id, status=new_status)

    async def update_version_params(self, version_id: UUID, new_params: VersionParamsRequest):
        """_summary_

        Args:
            version_id (UUID): _description_
            new_params (dict): _description_

        Returns:
            _type_: _description_
        """
        params_json = new_params.model_dump_json()
        return await self.version_repo.async_update(version_id, params=params_json)

    async def upload_version_file(self, version_id: UUID,
                                  file: UploadFile,
                                  is_data_file: bool = True):
        """_summary_

        Args:
            version_id (UUID): _description_
            file (UploadFile): _description_
            is_data_file (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        # Construct the version-specific directory path
        version_dir = self.base_result_dir / str(version_id)
        data_dir = version_dir / 'data'
        result_dir = version_dir / 'result'

        # Create the directories if they don't exist
        data_dir.mkdir(parents=True, exist_ok=True)
        result_dir.mkdir(parents=True, exist_ok=True)

        # Determine the subdirectory and file path
        sub_dir = data_dir if is_data_file else result_dir
        file_path = sub_dir / file.filename

        # Save the file
        async with aiofiles.open(file_path, 'wb') as buffer:
            # Read chunks of 1024 bytes
            while content := await file.read(1024):
                await buffer.write(content)

        return str(file_path)

    async def calculate_version(self, version_id: UUID):
        """_summary_

        Args:
            version_id (UUID): _description_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        print(type(version_id))
        version = await self.version_repo.async_get(version_id)
        if not version:
            raise ValueError("Version not found")

        # Configure STSConfig with version params
        sts_config = STSConfig(version_id=version_id,
                               json_config=version.params)

        # Create and start the process
        sts_controller = STSProcessController(sts_config)
        sts_controller.start_process()

        # Retrieve process output
        output, errors = sts_controller.get_output()

        return output, errors
