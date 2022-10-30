import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_expects_json import expects_json
from flask_migrate import Migrate
import requests
import sys
import json
from constants.messages import *
from config import config
from constants.gutendex import *
from review_controller import *

app = Flask(__name__)
app.config.from_object(config.get('dev'))
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def open_schema_file():
    try:
        os.chdir(os.getcwd().replace('/tests', '/'))
        with open('schemas/review.json', 'r') as file:
            return json.load(file)
    except OSError:
        print('Could not open the schema file')
        sys.exit()


review_schema = open_schema_file()


def calculate_average_rating(review_list):
    try:
        return round(sum(r.rating for r in review_list) / len(review_list), 1)
    except ZeroDivisionError:
        return NO_RATING
    except:
        return RATING_ERROR


def get_rating_and_review(review_list, book_details_response):
    if type(review_list) == dict and 'error' in review_list.keys():
        return {'rating': LOADING_RATING_ERROR, 'reviews': LOADING_REVIEW_ERROR}
    elif review_list:
        return {'rating': calculate_average_rating(review_list), 'reviews': [r.review for r in review_list]}
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
        from review_controller import save_review
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
    uri = GUTENDEX_BOOK_SEARCH_URL + bookname
    response = requests.get(uri)
    return filtered_response(response.json())


def request_gutendex_by_id(book_id):
    try:
        uri = GUTENDEX_BOOKS_URL + book_id
        response = requests.get(uri)
        if response.status_code == 404:
            return [{'booking details': 'The book id {} is not valid'.format(book_id)}]
        elif response.status_code == 500:
            return [{'booking details': GUTENDEX_API_ERR}]
        return filtered_response(response.json())
    except:
        return [{'booking details': UNKNOWN_ERROR}]


if __name__ == '__main__':
    from models import Review
    db.create_all()
    app.run()
