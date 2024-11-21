"""
Module for database operations
"""


from sqlmodel import create_engine, SQLModel, Session
from .user import User
from .pitch import Pitch
from .city import City
from .pitch_owner import PitchOwner
from .reservation import Reservation
from .review import Review
import os


database_url = os.getenv("ODBCConnectionString")

def create_engine_db():
    """Create the engine to connect to the database"""
    return create_engine(database_url)
    
def create_database_tables(engine):
    """Create the tables in the database"""
    SQLModel.metadata.create_all(engine)
    
def get_session():
    """Get the session to interact with the database"""
    with Session(engine) as session:
        yield session
    
engine = create_engine_db()