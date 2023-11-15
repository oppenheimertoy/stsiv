"""
This module contains Version model implementation
"""
from __future__ import annotations
from uuid import uuid4, UUID
from typing import TYPE_CHECKING, Any

from sqlalchemy import String
from sqlalchemy import UUID as UUID_SQL

from sqlalchemy import (
    ForeignKey,
    JSON
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from core.database.database import Base as BaseModel
from core.database.mixins.timestamps import TimestampMixin


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
        UUID_SQL, ForeignKey("experimets.id"))
    name: Mapped[str] = mapped_column(
        String, default="Version Template")  # add autonaming later
    description: Mapped[str] = mapped_column(String, default="")
    params: Mapped[Any] = mapped_column(JSON) # params for certain version num
