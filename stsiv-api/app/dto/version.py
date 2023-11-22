"""
Module contains realizations of DTO classes using for Comment abstraction
"""
from uuid import UUID
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class VersionDataDTO:
    """_summary_
    """
    experiment_id: UUID
    name: str
    description: str
