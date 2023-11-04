# pylint: skip-file
"""
Module contains realisation of Mixin class for created_at and 
updated_at properties
"""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr


class TimestampMixin:
    """
    This class declaring service attributes for all
    application models. This could potentialy help 
    with some debugging issues and I think it is
    a good practice
    """
    @declared_attr
    def created_at(cls):
        """
        Mark a class-level method for object creation time. 
        Returns:
            sqlalchemy.Column: created_at attribute for service models 
        """
        return Column(DateTime(timezone=True),
                      default=datetime.now(tz=timezone.utc),
                      nullable=False)

    @declared_attr
    def updated_at(cls):
        """
        Mark a class-level method for object update time.
        Returns:
            sqlalchemy.Column: created_at attribute for service models 
        """
        return Column(
            DateTime(timezone=True),
            default=datetime.now(tz=timezone.utc),
            onupdate=datetime.now(tz=timezone.utc),
            nullable=False
        )