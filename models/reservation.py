"""
Module of Reservation objects
"""


from .base_model import BaseModel
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING
from datetime import datetime
from enum import Enum


if TYPE_CHECKING:
    from .user import User
    from .pitch import Pitch


class Status(str, Enum):
    """Enum of status values"""
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELED = 'canceled'
    
    
class Reservation(BaseModel, table=True):
    """Class of Reservation objects"""
    
    
    pitch_id: str = Field(default=None, foreign_key='pitch.id', nullable=False, max_length=128)
    user_id: str = Field(default=None, foreign_key='user.id', nullable=False, max_length=128)
    start_time: datetime = Field(default=None, nullable=False, unique=True)
    status: Status = Field(default=Status.PENDING, nullable=False)
    user: 'User' = Relationship(back_populates='reservations')
    pitch: 'Pitch' = Relationship(back_populates='reservations')