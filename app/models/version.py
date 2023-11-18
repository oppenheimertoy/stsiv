"""
This module contains Version model implementation
"""
from __future__ import annotations
import json
from uuid import uuid4, UUID
from typing import TYPE_CHECKING, Any
from enum import Enum as PyEnum

from sqlalchemy import String
from sqlalchemy import UUID as UUID_SQL

from sqlalchemy import (
    ForeignKey,
    JSON,
    Enum
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from core.database.database import Base as BaseModel
from core.database.mixins.timestamps import TimestampMixin


if TYPE_CHECKING:
    from .experiment import Experiment
    from .test_result import TestResult
else:
    Experiment = "Experiment"
    TestResult = "TestResult"


class VersionStatus(PyEnum):
    WAITING = "waiting"
    SUCCESSFUL = "successful"
    ERROR = "error"


default_params = json.loads("""{
    "tests": {
        "alias": "-t",
        "value": [0]
    },
    "parameters": {
        "alias": "-P",
        "blockFrequencyTestBlockLength": {
            "id": "1",
            "value": 16384
        },
        "nonOverlappingTemplateTestBlockLength":{
            "id": "2",
            "value": 9
        },
        "overlappingTemplateTestBlockLength": {
            "id": "3",
            "value": 9
        },
        "approximateEntropyTestBlockLength": {
            "id": "4",
            "value": 10
        },
        "serialTestBlockLength": {
            "id": "5",
            "value": 16
        },
        "linearComplexityTestBlockLength": {
            "id": "6",
            "value": 500
        },
        "numberOfBitcountRuns": {
            "id": "7",
            "value": 1
        },
        "uniformityBins": {
            "id": "8",
            "value": 18.12
        },
        "bitsToProcessPerIteration": {
            "id": "9",
            "value": 1048576
        },
        "uniformityCutoffLevel": {
            "id": "10",
            "value": 0.0001
        },
        "alphaConfidenceLevel": {
            "id": "11",
            "value": 0.01
        }
    },
    "iterations": {
        "alias": "-i",
        "value": 1000
    },
    "workDir": {
        "alias": "-w",
        "value": "."
    },
    "createResultFiles": {
        "alias": "-s",
        "value": ""
    },
    "bitcount": {
        "alias": "-S",
        "value": 1048576
    },
    "numOfThreads": {
        "alias": "-T",
        "value": 1
    }
}""")


class Version(BaseModel, TimestampMixin):
    """_summary_

    Args:
        BaseModel (_type_): _description_
        TimestampMixin (_type_): _description_
    """
    __tablename__ = "versions"
    id: Mapped[UUID] = mapped_column(
        UUID_SQL, primary_key=True, default=uuid4)
    experiment_id: Mapped[UUID] = mapped_column(
        UUID_SQL, ForeignKey("experiments.id"))
    name: Mapped[str] = mapped_column(
        String, default="Version Template")  # add autonaming later
    description: Mapped[str] = mapped_column(String, default="")
    params: Mapped[Any] = mapped_column(
        JSON, default=default_params)  # params for certain version num
    status: Mapped[PyEnum] = mapped_column(
        Enum(VersionStatus), default=VersionStatus.WAITING)

    experiments_parent_rel: Mapped[Experiment] = relationship(
        back_populates="versions_child_rel")

    tests_result_child_rel: Mapped[TestResult] = relationship(
        back_populates="versions_parent_rel")
