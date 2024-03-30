from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class City(BaseModel, Base):
    """Representation of city """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)