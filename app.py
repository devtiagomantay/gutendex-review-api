
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import requests
from flask_expects_json import expects_json

app = Flask(__name__)
db = SQLAlchemy(app)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(500))


schema = {
    "type": "object",
    "properties": {
        "bookId": {"type": "number"},
        "rating": {"type": "number"},
        "review": {"type": "string"},
    },
    "required": ["bookId", "rating", "review"]
}


def search_review(book_id):
    try:
        review_ = Review.query.filter_by(book_id=book_id).all()
        return review_
    except Exception as e:
        return ['A unexpected error occurred loading reviews: ' + e]


def calculate_average_rating(review_list):
    try:
        return round(sum(r.rating for r in review_list) / len(review_list), 1)
    except Exception:
        return '-'


def get_user_reviews(review_list):
    try:
        return [r.review for r in review_list]
    except Exception as e:
        return ['A unexpected error occurred loading reviews: ' + e]


@app.route('/books/details/<book_id>')
def search_details(book_id):
    review_list = search_review(book_id)
    book_details_response = request_gutendex_by_id(book_id)
    book_details_response[0]['rating'] = calculate_average_rating(review_list)
    book_details_response[0]['reviews'] = get_user_reviews(review_list)
    return book_details_response


@app.route('/books/review', methods=['POST'])
@expects_json(schema)
def review():
    try:
        payload = request.json
        save_review(payload)
        return 'The review for the book {} has been saved'.format(payload['bookId'])
    except Exception:
        return 'A unexpected error occurred saving the review for the book: {}'.format(payload['bookId'])


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
        return filtered_response(response.json())
    except Exception:
        return ''


def save_review(payload):
    review_ = Review(book_id=payload['bookId'], rating=payload['rating'], review=payload['review'])
    db.session.add(review_)
    db.session.commit()


if __name__ == '__main__':
    db.create_all()
    app.run()
