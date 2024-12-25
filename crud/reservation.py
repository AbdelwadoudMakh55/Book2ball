"""
Module of Reservation CRUD operations
"""

from models.reservation import Reservation
from models.database import engine
from sqlmodel import Session, select
from datetime import datetime

time = "%Y-%m-%dT%H:%M:%S.%f"


def get_all_reservations():
    """
    Get all reservations from the database
    """
    with Session(engine) as session:
        statement = select(Reservation)
        reservations = session.exec(statement).all()
        reservations = [reservation.to_dict() for reservation in reservations]
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
        reservations = [reservation.to_dict() for reservation in reservations]
    return reservations

def get_reservations_by_pitch_id(pitch_id: str, date: str = None):
    """
    Get reservations by pitch id
    """
    with Session(engine) as session:
        statement = select(Reservation).where(Reservation.pitch_id == pitch_id)
        reservations = session.exec(statement).all()
        pitch_reservations_by_day = []
        if date:
            for reservation in reservations:
                start_time = datetime.strptime(reservation.start_time, time)
                if start_time.date() != datetime.strptime(date, "%Y-%m-%d").date():
                    pitch_reservations_by_day.append(reservation)
            return pitch_reservations_by_day
    return reservations

def get_reservation_by_start_time(pitch_id: str, start_time: str):
    """
    Get a reservation by its start time
    """
    start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    with Session(engine) as session:
        statement = select(Reservation).where(Reservation.pitch_id == pitch_id).where(Reservation.start_time == start_time)
        reservation = session.exec(statement).first()
    return reservation

def get_reservations_by_status(status: str):
    """
    Get reservations by status
    """
    with Session(engine) as session:
        statement = select(Reservation).where(Reservation.status == status)
        reservations = session.exec(statement).all()
    return reservations

def create_reservation_db(**kwargs):
    """
    Create a new reservation in the database
    """
    reservation = Reservation(**kwargs)
    with Session(engine) as session:
        session.add(reservation)
        session.commit()
        session.refresh(reservation)
    return reservation

def update_reservation(reservation_id, **kwargs):
    """
    Update an existing reservation in the database
    """
    reservation = get_reservation_by_id(reservation_id)
    with Session(engine) as session:
        for key, value in kwargs.items():
            setattr(reservation, key, value)
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