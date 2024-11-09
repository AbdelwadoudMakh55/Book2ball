import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class User(BaseModel, Base):
    """Representation of user """
    __tablename__ = 'users'
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    phone = Column(String(128), nullable=False)
    city_id = Column(String(128), ForeignKey('cities.id'), nullable=False)
    reservations = relationship("Reservation", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes User"""
        super().__init__(*args, **kwargs)

    @property
    def reservations(self):
        """getter attribute returns the list of Reservation instances"""
        from models.reservation import Reservation
        reservation_list = []
        all_reservations = models.storage.all(Reservation)
        for reservation in all_reservations.values():
            if reservation.user_id == self.id:
                reservation_list.append(reservation)
        return reservation_list