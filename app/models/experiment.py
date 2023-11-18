"""
This module contains Experiment model implementation
"""
from __future__ import annotations
from uuid import uuid4, UUID
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy import UUID as UUID_SQL, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from core.database.database import Base as BaseModel
from core.database.mixins.timestamps import TimestampMixin

if TYPE_CHECKING:
    from .user import User
    from .version import Version
else:
    User = "User"
    Version = "Version"


class Experiment(BaseModel, TimestampMixin):
    """_summary_

    Args:
        BaseModel (_type_): _description_
        TimestampMixin (_type_): _description_
    """
    __tablename__ = "experiments"
    id: Mapped[UUID] = mapped_column(
        UUID_SQL, primary_key=True, default=uuid4)
    # foreign key for this users table
    creator_id: Mapped[UUID] = mapped_column(UUID_SQL, ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, default="")
    versions_num: Mapped[int] = mapped_column(Integer, default=0)

    users_parent_rel: Mapped[User] = relationship(
        back_populates="experiments_child_rel")

    versions_child_rel: Mapped[Version] = relationship(
        back_populates="experiments_parent_rel")
