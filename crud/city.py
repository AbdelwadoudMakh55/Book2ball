"""
Module of City CRUD operations
"""

from models.city import City
from models.database import engine
from sqlmodel import Session, select
from datetime import datetime

def get_all_cities():
    """
    Get all cities from the database
    """
    with Session(engine) as session:
        statement = select(City)
        cities = session.exec(statement).all()
        cities = [city.to_dict() for city in cities]
    return cities

def get_city_by_id(city_id: str):
    """
    Get a city by its id
    """
    with Session(engine) as session:
        statement = select(City).where(City.id == city_id)
        city = session.exec(statement).first()
    return city

def get_city_by_name(city_name: str):
    """
    Get a city by its name
    """
    with Session(engine) as session:
        statement = select(City).where(City.name == city_name)
        city = session.exec(statement).first()
    return city

def create_city(**kwargs):
    """
    Create a new city
    """
    with Session(engine) as session:
        new_city = City(**kwargs)
        session.add(new_city)
        session.commit()
        session.refresh(new_city)
    return new_city

def update_city(city_id: str, **kwargs):
    """
    Update an existing city
    """
    with Session(engine) as session:
        statement = select(City).where(City.id == city_id)
        city = session.exec(statement).first()
        for key in kwargs:
            if key not in ['name']:
                pass
            else:
                setattr(city, key, kwargs[key])
        setattr(city, 'updated_at', datetime.now())
        session.add(city)
        session.commit()
        session.refresh(city)
    return city

def delete_city(city_id: str):
    """
    Delete a city
    """
    with Session(engine) as session:
        statement = select(City).where(City.id == city_id)
        city = session.exec(statement).first() 
        session.delete(city)
        session.commit()

def get_pitches_by_city_id(city_id: str):
    """
    Get all pitches in a city
    """
    with Session(engine) as session:
        statement = select(City).where(City.id == city_id)
        city = session.exec(statement).first()
        pitches = [pitch.to_dict() for pitch in city.pitches]
    return pitches

def get_users_by_city_id(city_id: str):
    """
    Get all users in a city
    """
    with Session(engine) as session:
        statement = select(City).where(City.id == city_id)
        city = session.exec(statement).first()
        users = [user.to_dict() for user in city.users]
    return users

def get_pitch_owners_by_city_id(city_id: str):
    """
    Get all pitch owners in a city
    """
    with Session(engine) as session:
        statement = select(City).where(City.id == city_id)
        city = session.exec(statement).first()
        pitch_owners = [pitch_owner.to_dict() for pitch_owner in city.pitch_owners]
    return pitch_owners