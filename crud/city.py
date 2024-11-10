"""
Module of City CRUD operations
"""

from models.city import City
from models.database import engine
from sqlmodel import Session, select


def get_all_cities():
    """
    Get all cities from the database
    """
    with Session(engine) as session:
        statement = select(City)
        cities = session.exec(statement).all()
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

def create_city(city: City):
    """
    Create a new city
    """
    with Session(engine) as session:
        session.add(city)
        session.commit()
        session.refresh(city)
    return city

def update_city(**kwargs):
    """
    Update an existing city
    """
    city = City(**kwargs)
    with Session(engine) as session:
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
    return city