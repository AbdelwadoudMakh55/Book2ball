"""
Module of City Objects
"""


from typing import TYPE_CHECKING
from .base_model import BaseModel
from sqlmodel import Field, Relationship


if TYPE_CHECKING:
    from .pitch import Pitch
    from .user import User
    from .pitch_owner import PitchOwner

class City(BaseModel, table=True):
    """City Class"""
        
    name: str = Field(default=None, nullable=False)
    pitches: list["Pitch"] = Relationship(back_populates='city')
    users: list["User"] = Relationship(back_populates='city')
    pitch_owners: list["PitchOwner"] = Relationship(back_populates='city')