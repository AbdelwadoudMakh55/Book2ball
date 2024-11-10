"""
Module of Reservation CRUD operations
"""

from models.reservation import Reservation
from models.database import engine
from sqlmodel import Session, select


def get_all_reservations():
    """
    Get all reservations from the database
    """
    with Session(engine) as session:
        statement = select(Reservation)
        reservations = session.exec(statement).all()
    return reservations

def get_reservation_by_id(reservation_id: str):
    """
    Get a reservation by its id
    """
    with Session(engine) as session:
        statement = select(Reservation).where(Reservation.id == reservation_id)
        reservation = session.exec(statement).first()
    return reservation

def get_reservations_by_user_id(user_id: str):
    """
    Get reservations by user id
    """
    with Session(engine) as session:
        statement = select(Reservation).where(Reservation.user_id == user_id)
        reservations = session.exec(statement).all()
    return reservations

def get_reservations_by_pitch_id(pitch_id: str):
    """
    Get reservations by pitch id
    """
    with Session(engine) as session:
        statement = select(Reservation).where(Reservation.pitch_id == pitch_id)
        reservations = session.exec(statement).all()
    return reservations

def create_reservation(reservation: Reservation):
    """
    Create a new reservation in the database
    """
    with Session(engine) as session:
        session.add(reservation)
        session.commit()
        session.refresh(reservation)
    return reservation

def update_reservation(**kwargs):
    """
    Update an existing reservation in the database
    """
    reservation = Reservation(**kwargs)
    with Session(engine) as session:
        session.add(reservation)
        session.commit()
        session.refresh(reservation)
    return reservation

def delete_reservation(reservation_id: str):
    """
    Delete a reservation from the database
    """
    with Session(engine) as session:
        reservation = get_reservation_by_id(reservation_id)
        if reservation:
            session.delete(reservation)
            session.commit()
    return reservation