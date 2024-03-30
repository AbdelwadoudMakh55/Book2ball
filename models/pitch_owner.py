import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Pitch_Owner(BaseModel, Base):
    """Representation of pitch owner """
    __tablename__ = 'pitch_owners'
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    phone = Column(String(128), nullable=False)
    address = Column(String(128), nullable=False)
    pitches = relationship("Pitch",
                           backref="pitch_owner",
                           cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes PitchOwner"""
        super().__init__(*args, **kwargs)

    @property
    def pitches(self):
        """getter attribute returns the list of Pitch instances"""
        from models.pitch import Pitch
        pitch_list = []
        all_pitches = models.storage.all(Pitch)
        for pitch in all_pitches.values():
            if pitch.pitchOwner_id == self.id:
                pitch_list.append(pitch)
        return pitch_list
