from flask_sqlalchemy import SQLAlchemy
from app import db


class Review(db.Model):
    """Review model"""
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(500))
