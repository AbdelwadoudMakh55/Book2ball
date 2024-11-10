"""
Module of User Objects
"""


from .base_model import BaseModel
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


if TYPE_CHECKING:
    from .reservation import Reservation
    from .city import City
    

class User(BaseModel, table=True):
    """Class of user"""
    
    name: str = Field(default=None, nullable=False)
    email: EmailStr = Field(default=None, nullable=False)
    phone: PhoneNumber = Field(default=None, nullable=False)
    is_verified: bool = Field(default=False, nullable=False)
    city_id: str = Field(default=None, nullable=False, foreign_key='city.id', max_length=128)
    city: 'City' = Relationship(back_populates='users')
    reservations: list['Reservation'] = Relationship(back_populates='user')