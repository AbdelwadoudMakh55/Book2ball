import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Representation of city """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    pitches = relationship('Pitch', backref='city', cascade='all, delete-orphan')
    users = relationship('User', backref='city', cascade='all, delete-orphan')
    pitch_owners = relationship('PitchOwner', backref='city', cascade='all, delete-orphan')

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)

    @property
    def pitches(self):
        """getter attribute that returns the list of pitch instances with city_id"""
        from models.pitch import Pitch
        pitch_list = []
        all_pitches = models.storage.all(Pitch)
        for pitch in all_pitches.values():
            if pitch.city_id == self.id:
                pitch_list.append(pitch)
        return pitch_list
        
    @property
    def users(self):
        """getter attribute that returns the list of user instances with city_id"""
        from models.user import User
        user_list = []
        all_users = models.storage.all(User)
        for user in all_users.values():
            if user.city_id == self.id:
                user_list.append(user)
        return user_list

    @property
    def pitch_owners(self):
        """getter attribute that returns the list of pitch_owner instances with city_id"""
        from models.pitch_owner import PitchOwner
        pitch_owner_list = []
        all_pitch_owners = models.storage.all(PitchOwner)
        for pitch_owner in all_pitch_owners.values():
            if pitch_owner.city_id == self.id:
                pitch_owner_list.append(pitch_owner)
        return pitch_owner_list
