from main import db
from models import Review
import sqlalchemy.exc
from constants.messages import *


def save_review(payload):
    try:
        review_ = Review(book_id=payload['bookId'], rating=payload['rating'], review=payload['review'])
        db.session.add(review_)
        db.session.commit()
    except sqlalchemy.exc.OperationalError:
        # let the developers know asap ;)
        raise Exception('Error connecting database')
    except sqlalchemy.exc.ProgrammingError:
        # check database creation
        raise Exception('Database don\'t exists')
    except Exception as e:
        raise Exception(UNKNOWN_ERROR + 'detail: ' + e)


def search_review(book_id):
    try:
        review_ = Review.query.filter_by(book_id=book_id).all()
        return review_
    except:
        return {'error': LOADING_REVIEW_ERROR}
