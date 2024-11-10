"""
Module for Review Objetcs
"""


from .base_model import BaseModel
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING
from datetime import datetime


if TYPE_CHECKING:
    from .pitch import Pitch


class Review(BaseModel, table=True):
    """Class of review"""

    pitch_id: str = Field(default=None, foreign_key='pitch.id', nullable=False, max_length=128)
    comment: str = Field(default=None, nullable=False)
    rating: int = Field(default=None, nullable=False)
    date: datetime = Field(default_factory=datetime.now, nullable=False)
    pitch: 'Pitch' = Relationship(back_populates='reviews')