import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Pitch(BaseModel, Base):
    """Representation of pitch """
    __tablename__ = 'pitches'
    name = Column(String(128), nullable=False)
    location = Column(String(200), nullable=False)
    type = Column(String(128), nullable=False)
    capacity = Column(Integer, nullable=False)
    availability = Column(Boolean, nullable=False, default=True)
    pitchOwner_id = Column(String(128), ForeignKey('pitch_owners.id'), nullable=False)
    city_id = Column(String(128), ForeignKey('cities.id'), nullable=False)
    reviews = relationship("Review",
                            backref="pitch",
                            cascade="all, delete, delete-orphan")
    reservations = relationship("Reservation",
                            backref="pitch",
                            cascade="all, delete, delete-orphan")

    
    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)

    @property
    def reviews(self):
        """getter attribute returns the list of Review instances"""
        from models.review import Review
        review_list = []
        all_reviews = models.storage.all(Review)
        for review in all_reviews.values():
            if review.place_id == self.id:
                review_list.append(review)
        return review_list
    
    @property
    def reservations(self):
        """getter attribute returns the list of Reservation instances"""
        from models.reservation import Reservation
        reservation_list = []
        all_reservations = models.storage.all(Reservation)
        for reservation in all_reservations.values():
            if reservation.pitch_id == self.id:
                reservation_list.append(reservation)
        return reservation_list