"""
This module contains Version model implementation
"""
from __future__ import annotations
from uuid import uuid4, UUID
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy import UUID as UUID_SQL, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from core.database.database import Base as BaseModel
from core.database.mixins.timestamps import TimestampMixin



# amount of test in 