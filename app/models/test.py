"""
This module contains Test model implementation
"""
from uuid import uuid4, UUID

from sqlalchemy import String, Integer
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy.orm import Mapped, mapped_column

from core.database.database import Base as BaseModel
from core.database.mixins.timestamps import TimestampMixin


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

    def __repr__(self):
        return f"Test(id={self.id!r}, identifier={self.identifier!r}, name={self.name!r})"