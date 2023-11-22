"""
This module contains Test model implementation
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import uuid4, UUID

from sqlalchemy import String, Integer
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from core.database.database import Base as BaseModel
from core.database.mixins.timestamps import TimestampMixin

if TYPE_CHECKING:
    from .test_result import TestResult
else:
    TestResult = "TestResult"


class Test(BaseModel, TimestampMixin):
    """_summary_

    Args:
        BaseModel (_type_): _description_
        TimestampMixin (_type_): _description_
    """
    __tablename__ = "tests"
    id: Mapped[UUID] = mapped_column(
        UUID_SQL, primary_key=True, default=uuid4)
    identifier: Mapped[int] = mapped_column(Integer, unique=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    tests_result_child_rel: Mapped[TestResult] = relationship(
        back_populates="tests_parent_rel")

    def __repr__(self):
        return f"Test(id={self.id!r}, identifier={self.identifier!r}, name={self.name!r})"
