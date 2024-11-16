"""
Module of Pitch CRUD operations
"""

from models.pitch import Pitch
from models.database import engine
from sqlmodel import Session, select


def get_all_pitches():
    """
    Get all pitches from the database
    """
    with Session(engine) as session:
        statement = select(Pitch)
        pitches = session.exec(statement).all()
        pitches = [pitch.to_dict() for pitch in pitches]
    return pitches

def get_pitch_by_id(pitch_id: str):
    """
    Get a pitch by its id
    """
    with Session(engine) as session:
        statement = select(Pitch).where(Pitch.id == pitch_id)
        pitch = session.exec(statement).first()
    return pitch

def get_pitch_by_name(pitch_name: str):
    """
    Get a pitch by its name
    """
    with Session(engine) as session:
        statement = select(Pitch).where(Pitch.name == pitch_name)
        pitch = session.exec(statement).first()
    return pitch

def create_pitch_db(**kwargs):
    """
    Create a new pitch in the database
    """
    pitch = Pitch(**kwargs)
    with Session(engine) as session:
        session.add(pitch)
        session.commit()
        session.refresh(pitch)
    return pitch

def update_pitch(pitch_id: str, **kwargs):
    """
    Update an existing pitch in the database
    """
    pitch = get_pitch_by_id(pitch_id)
    with Session(engine) as session:
        for key, value in kwargs.items():
            setattr(pitch, key, value)
        session.add(pitch)
        session.commit()
        session.refresh(pitch)
    return pitch

def delete_pitch(pitch_id: str):
    """
    Delete a pitch from the database
    """
    with Session(engine) as session:
        pitch = get_pitch_by_id(pitch_id)
        if pitch:
            session.delete(pitch)
            session.commit()