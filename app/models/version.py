"""
This module contains Version model implementation
"""
from __future__ import annotations
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
from app.services.argument_parser.args_parsed import default_params

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
