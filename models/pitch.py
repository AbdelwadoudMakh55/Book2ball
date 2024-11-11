"""
Module of Pitch Objects
"""


from .base_model import BaseModel
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .review import Review
    from .reservation import Reservation
    from .pitch_owner import PitchOwner
    from .city import City
    
class Capacity(int, Enum):
    """ Capacity Enum """
    SMALL = 10
    MEDIUM = 16
    LARGE = 22

class Pitch(BaseModel, table=True):
    """Class of Pitch Objects"""
    
    name: str = Field(default=None, nullable=False)
    location: str = Field(default=None, nullable=False)
    capacity: Capacity = Field(default=None, nullable=False)
    availability: bool = Field(default=True, nullable=False)
    pitchOwner_id: str = Field(default=None, foreign_key='pitchowner.id', nullable=False, max_length=128)
    city_id: str = Field(default=None, foreign_key='city.id', nullable=False, max_length=128)
    city: 'City' = Relationship(back_populates='pitches')
    pitchOwner: 'PitchOwner' = Relationship(back_populates='pitches')
    reviews: list["Review"] = Relationship(back_populates='pitch')
    reservations: list["Reservation"] = Relationship(back_populates='pitch')