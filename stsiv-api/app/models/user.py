"""
This module contains User model implementation
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import uuid4, UUID

from sqlalchemy import String, Boolean
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from core.database.database import Base as BaseModel
from core.database.mixins.timestamps import TimestampMixin


if TYPE_CHECKING:
    from .experiment import Experiment
else:
    Experiment = "Experiment"


class User(BaseModel, TimestampMixin):
    """
    This class is implementation of User model
    Args:
        BaseModel (metaclass): declarative base
    """
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(
        UUID_SQL, primary_key=True, default=uuid4)
    username: Mapped[String] = mapped_column(String, unique=True)
    email: Mapped[String] = mapped_column(String, unique=True)
    _password: Mapped[String] = mapped_column("password", String)
    name: Mapped[String] = mapped_column(String)
    surname: Mapped[String] = mapped_column(String)
    active: Mapped[Boolean] = mapped_column(Boolean, default=True)

    experiments_child_rel: Mapped[Experiment] = relationship(
        back_populates="users_parent_rel")

    @property
    def password(self) -> str:
        """
        Propety for password attribute

        Raises:
            AttributeError: raising attribure error if password is corrupted
        """
        return self._password

    def __repr__(self):
        return f"<User(user)(user_id={self.id}, username={self.username}, \
            email={self.email}, status={self.active})"
