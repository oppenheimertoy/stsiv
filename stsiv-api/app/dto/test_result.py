"""
Module contains realizations of DTO classes using for Comment abstraction
"""
from uuid import UUID
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class TestResultDataDTO:
    """_summary_
    """
    version_id: UUID
    test_id: UUID
