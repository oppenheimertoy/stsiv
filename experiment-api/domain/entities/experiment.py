"""
This module contains Experiment model implementation
"""
from uuid import uuid4, UUID

from sqlalchemy import String
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.database import Base as BaseModel
from core.database.mixins import TimestampMixin

class Experiment(BaseModel, TimestampMixin):
    """
    Model for experiment entity.
    """
    __tablename__ = "experiments"
    id: Mapped[UUID] = mapped_column(UUID_SQL, primary_key=True, default=uuid4())
    name: Mapped[str] = mapped_column(String, unique=False)
    user_id: Mapped[UUID] = mapped_column(UUID_SQL) # foreign key to user service
    description: Mapped[str] = mapped_column(TEXT)
    