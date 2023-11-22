"""
This module contains TestResult model implementation
"""
from __future__ import annotations
from uuid import uuid4, UUID
from typing import TYPE_CHECKING

from sqlalchemy import UUID as UUID_SQL, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from core.database.database import Base as BaseModel
from core.database.mixins.timestamps import TimestampMixin

if TYPE_CHECKING:
    from .version import Version
    from .test import Test
else:
    Test = "Test"
    Version = "Version"


class TestResult(BaseModel, TimestampMixin):
    """_summary_

    Args:
        BaseModel (_type_): _description_
        TimestampMixin (_type_): _description_
    """
    __tablename__ = "test_results"
    id: Mapped[UUID] = mapped_column(
        UUID_SQL, primary_key=True, default=uuid4)
    # foreign key for this users table
    version_id: Mapped[UUID] = mapped_column(UUID_SQL, ForeignKey("versions.id"))
    test_id: Mapped[UUID] = mapped_column(UUID_SQL, ForeignKey("tests.id"))

    versions_parent_rel: Mapped[Version] = relationship(
        back_populates="tests_result_child_rel")

    tests_parent_rel: Mapped[Test] = relationship(
        back_populates="tests_result_child_rel")
