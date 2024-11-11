"""
Module of User CRUD operations
"""

from models.user import User
from models.database import engine
from sqlmodel import Session, select


def get_all_users():
    """
    Get all users from the database
    """
    with Session(engine) as session:
        statement = select(User)
        users = session.exec(statement).all()
        users = [user.to_dict() for user in users]
    return users

def get_user_by_id(user_id: str):
    """
    Get a user by its id
    """
    with Session(engine) as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
    return user

def get_user_by_email(email: str):
    """
    Get a user by its email
    """
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
    return user

def create_user_db(**kwargs) -> User:
    """
    Create a new user in the database
    """
    new_user = User(**kwargs)
    with Session(engine) as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

def update_user(user_id: str, **kwargs):
    """
    Update an existing user in the database
    """
    user = get_user_by_id(user_id)
    for key, value in kwargs.items():
        setattr(user, key, value)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def delete_user(user_id: str):
    """
    Delete a user from the database
    """
    with Session(engine) as session:
        user = get_user_by_id(user_id)
        if user:
            session.delete(user)
            session.commit()