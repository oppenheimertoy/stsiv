"""
This module contains Experiment model implementation
"""
from uuid import uuid4, UUID

from sqlalchemy import String, Integer
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy.orm import Mapped, mapped_column

from core.database.database import Base as BaseModel
from core.database.mixins.timestamps import TimestampMixin


class Experiment(BaseModel, TimestampMixin):
    """_summary_

    Args:
        BaseModel (_type_): _description_
        TimestampMixin (_type_): _description_
    """
    __tablename__ = "experiments"
    id: Mapped[UUID] = mapped_column(
        UUID_SQL, primary_key=True, default=uuid4)
    creator_id: UUID = mapped_column