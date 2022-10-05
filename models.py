from app import db


class Review(db.Model):
    """Review model"""
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(500))

    def __init__(self, book_id, rating, review):
        self.book_id = book_id,
        self.rating = rating,
        self.review = review

    def __repr__(self):
        return '<id {}>'.format(self.id)
