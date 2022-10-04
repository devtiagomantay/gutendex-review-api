import http

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import requests
from flask_expects_json import expects_json

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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


@app.route('/books/review', methods=['POST'])
@expects_json(schema)
def review():
    try:
        payload = request.json
        save_review(payload)
        return 'The review for the book {} has been saved'.format(payload['bookId'])
    except Exception:
        return 'A unexpected error occurred saving the review for the book: {}'.format(payload['bookId'])


@app.route('/books/name/<book_name>')
def search_book(book_name):
    return request_gutendex(book_name)


def filtered_response(res):
    books = []
    for r in res['results']:
        d = {'id': r['id'], 'title': r['title'], 'authors': r['authors'], 'languages': r['languages'],
             'download_count': r['download_count']}
        books.append(d)

    return books


def request_gutendex(bookname):
    uri = 'https://gutendex.com/books?search=' + bookname
    response = requests.get(uri)
    return filtered_response(response.json())


def save_review(payload):
    review_ = Review(book_id=payload['bookId'], rating=payload['rating'], review=payload['review'])
    db.session.add(review_)
    db.session.commit()


if __name__ == '__main__':
    db.create_all()
    app.run()
