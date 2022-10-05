import sqlalchemy.exc
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_expects_json import expects_json
import requests
import sys
import json
from constants.messages import *
from config import config

app = Flask(__name__)
app.config.from_object(config.get('dev'))
db = SQLAlchemy(app)


def open_schema_file():
    try:
        with open('./schemas/review.json', 'r') as file:
            return json.load(file)
    except OSError:
        print('Could not open the schema file')
        sys.exit()


review_schema = open_schema_file()


def search_review(book_id):
    try:
        from models import Review
        review_ = Review.query.filter_by(book_id=book_id).all()
        return review_
    except:
        return {'error': LOADING_REVIEW_ERROR}


def calculate_average_rating(review_list):
    try:
        return round(sum(r.rating for r in review_list) / len(review_list), 1)
    except ZeroDivisionError:
        return NO_RATING
    except:
        return RATING_ERROR


def get_user_reviews(review_list):
    try:
        return [r.review for r in review_list]
    except:
        return [REVIEWS_UNKNOWN_ERROR]


def get_rating_and_review(review_list, book_details_response):
    if type(review_list) == dict and 'error' in review_list.keys():
        return {'rating': LOADING_RATING_ERROR, 'reviews': LOADING_REVIEW_ERROR}
    elif review_list:
        return {'rating': calculate_average_rating(review_list), 'reviews': get_user_reviews(review_list)}
    elif 'booking details' not in book_details_response[0].keys():
        return {'rating': NO_RATINGS_MSG, 'reviews': NO_REVIEWS_MSG}
    return None


@app.route('/books/details/id=<book_id>')
def search_details(book_id):
    review_list = search_review(book_id)
    book_details_response = request_gutendex_by_id(book_id)
    result = get_rating_and_review(review_list, book_details_response)
    if result:
        book_details_response[0]['rating'] = result['rating']
        book_details_response[0]['reviews'] = result['reviews']

    return book_details_response


@app.route('/books/review', methods=['POST'])
@expects_json(review_schema)
def review_post():
    try:
        payload = request.json
        save_review(payload)
        return 'The review for the book {} has been saved'.format(payload['bookId'])
    except:
        return SAVING_REVIEW_ERROR


@app.route('/books/search/name/<book_name>')
def search_book(book_name):
    return request_gutendex_by_bookname(book_name)


def filtered_response(res):
    books = []
    results = res['results'] if 'results' in res.keys() else [res]
    for r in results:
        d = {'id': r['id'], 'title': r['title'], 'authors': r['authors'], 'languages': r['languages'],
             'download_count': r['download_count']}
        books.append(d)

    return books


def request_gutendex_by_bookname(bookname):
    uri = 'https://gutendex.com/books?search=' + bookname
    response = requests.get(uri)
    return filtered_response(response.json())


def request_gutendex_by_id(book_id):
    try:
        uri = 'https://gutendex.com/books/' + book_id
        response = requests.get(uri)
        if response.status_code == 404:
            return [{'booking details': 'The book id {} is not valid'.format(book_id)}]
        elif response.status_code == 500:
            return [{'booking details': GUTENDEX_API_ERR}]
        return filtered_response(response.json())
    except:
        return [{'booking details': UNKNOWN_ERROR}]


def save_review(payload):
    try:
        from models import Review
        review_ = Review(book_id=payload['bookId'], rating=payload['rating'], review=payload['review'])
        db.session.add(review_)
        db.session.commit()
    except sqlalchemy.exc.OperationalError:
        # let the developers know asap ;)
        raise Exception('Error connecting database')
    except sqlalchemy.exc.ProgrammingError:
        # check database creation
        raise Exception('Database don\'t exists')
    except Exception:
        raise Exception('error')


if __name__ == '__main__':
    db.create_all()
    app.run()
