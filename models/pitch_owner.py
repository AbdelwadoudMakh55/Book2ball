"""
Module of PitchOwner objects
"""


from .base_model import BaseModel
from sqlmodel import Field, Relationship
from typing  import TYPE_CHECKING, Optional
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


if TYPE_CHECKING:
    from .pitch import Pitch
    
    
class PitchOwner(BaseModel, table=True):
    """PitchOwner class"""
    
    name: str = Field(default=None, nullable=False)
    email: EmailStr = Field(default=None, nullable=False)
    phone: PhoneNumber = Field(default=None, nullable=False)
    city_id: str = Field(default=None, nullable=False, foreign_key='city.id', max_length=128)
    pitches: list['Pitch'] = Relationship(back_populates='pitchOwner')