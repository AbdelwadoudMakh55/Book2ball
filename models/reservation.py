import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

class Reservation(BaseModel, Base):
    """Representation of reservation """
    __tablename__ = 'reservations'
    pitch_id = Column(String(128), ForeignKey('pitches.id'), nullable=False)
    user_id = Column(String(128), ForeignKey('users.id'), nullable=False)
    date = Column(String(128), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String(128), nullable=False)
    user = relationship("User", back_populates="reservations")
    pitch = relationship("Pitch", back_populates="reservations")

    def __init__(self, *args, **kwargs):
        """initializes Reservation"""
        super().__init__(*args, **kwargs)

    @property
    def user(self):
        """getter attribute returns the User instance"""
        from models.user import User
        user = models.storage.get(User, self.user_id)
        return user
    
    @property
    def pitch(self):
        """getter attribute returns the Pitch instance"""
        from models.pitch import Pitch
        pitch = models.storage.get(Pitch, self.pitch_id)
        return pitch