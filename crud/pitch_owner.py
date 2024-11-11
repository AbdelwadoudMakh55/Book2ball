"""
Module of PitchOwner CRUD operations
"""

from models.pitch_owner import PitchOwner
from models.pitch import Pitch
from models.database import engine
from sqlmodel import Session, select
from datetime import datetime


def get_all_pitch_owners():
    """
    Get all pitch owners from the database
    """
    with Session(engine) as session:
        statement = select(PitchOwner)
        pitch_owners = session.exec(statement).all()
        pitch_owners = [pitch_owner.to_dict() for pitch_owner in pitch_owners]
    return pitch_owners

def get_pitch_owner_by_id(pitch_owner_id: str):
    """
    Get a pitch owner by its id
    """
    with Session(engine) as session:
        statement = select(PitchOwner).where(PitchOwner.id == pitch_owner_id)
        pitch_owner = session.exec(statement).first()
    return pitch_owner

def get_pitch_owner_by_email(email: str):
    """
    Get a pitch owner by its email
    """
    with Session(engine) as session:
        statement = select(PitchOwner).where(PitchOwner.email == email)
        pitch_owner = session.exec(statement).first()
    return pitch_owner

def create_pitch_owner(**kwargs):
    """
    Create a new pitch owner in the database
    """
    pitch_owner = PitchOwner(**kwargs)
    with Session(engine) as session:
        session.add(pitch_owner)
        session.commit()
        session.refresh(pitch_owner)
    return pitch_owner

def update_pitch_owner(pitch_owner_id: str, **kwargs):
    """
    Update an existing pitch owner in the database
    """
    unchanged_attr = ['id', 'created_at', 'updated_at']
    with Session(engine) as session:
        pitch_owner = get_pitch_owner_by_id(pitch_owner_id)
        for key in kwargs.keys():
            if key not in unchanged_attr:
                setattr(pitch_owner, key, kwargs[key])
        setattr(pitch_owner, 'updated_at', datetime.now())
        session.add(pitch_owner)
        session.commit()
        session.refresh(pitch_owner)
    return pitch_owner

def delete_pitch_owner(pitch_owner_id: str):
    """
    Delete a pitch owner from the database
    """
    with Session(engine) as session:
        pitch_owner = get_pitch_owner_by_id(pitch_owner_id)
        if pitch_owner:
            session.delete(pitch_owner)
            session.commit()
            
def get_pitches_by_pitch_owner_id(pitch_owner_id: str):
    """
    Get all pitches by a pitch owner
    """
    with Session(engine) as session:
        statement = select(Pitch).where(Pitch.pitchOwner_id == pitch_owner_id)
        pitches = session.exec(statement).all()
        pitches = [pitch.to_dict() for pitch in pitches]
    return pitches