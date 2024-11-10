"""
Module of Review CRUD operations
"""

from models.review import Review
from models.database import engine
from sqlmodel import Session, select


def get_all_reviews():
    """
    Get all reviews from the database
    """
    with Session(engine) as session:
        statement = select(Review)
        reviews = session.exec(statement).all()
    return reviews

def get_review_by_id(review_id: str):
    """
    Get a review by its id
    """
    with Session(engine) as session:
        statement = select(Review).where(Review.id == review_id)
        review = session.exec(statement).first()
    return review


def get_reviews_by_pitch_id(pitch_id: str):
    """
    Get reviews by pitch id
    """
    with Session(engine) as session:
        statement = select(Review).where(Review.pitch_id == pitch_id)
        reviews = session.exec(statement).all()
    return reviews

def create_review(review: Review):
    """
    Create a new review in the database
    """
    with Session(engine) as session:
        session.add(review)
        session.commit()
        session.refresh(review)
    return review

def update_review(**kwargs):
    """
    Update an existing review in the database
    """
    review = Review(**kwargs)
    with Session(engine) as session:
        session.add(review)
        session.commit()
        session.refresh(review)
    return review

def delete_review(review_id: str):
    """
    Delete a review from the database
    """
    with Session(engine) as session:
        review = get_review_by_id(review_id)
        if review:
            session.delete(review)
            session.commit()
    return review