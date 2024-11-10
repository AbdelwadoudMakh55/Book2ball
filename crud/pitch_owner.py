"""
Module of PitchOwner CRUD operations
"""

from models.pitch_owner import PitchOwner
from models.database import engine
from sqlmodel import Session, select


def get_all_pitch_owners():
    """
    Get all pitch owners from the database
    """
    with Session(engine) as session:
        statement = select(PitchOwner)
        pitch_owners = session.exec(statement).all()
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

def create_pitch_owner(pitch_owner: PitchOwner):
    """
    Create a new pitch owner in the database
    """
    with Session(engine) as session:
        session.add(pitch_owner)
        session.commit()
        session.refresh(pitch_owner)
    return pitch_owner

def update_pitch_owner(**kwargs):
    """
    Update an existing pitch owner in the database
    """
    pitch_owner = PitchOwner(**kwargs)
    with Session(engine) as session:
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
    return pitch_owner