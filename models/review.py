from datetime import datetime
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey


class Review(BaseModel, Base):
    """Representation of Review """

    __tablename__ = 'reviews'
    reservation_id = Column(String(128), ForeignKey('reservations.id'), nullable=False)
    comment = Column(String(1024), nullable=False)
    rating = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.now(), nullable=False)


    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)