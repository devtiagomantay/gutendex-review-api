from flask import Flask, request
import requests

app = Flask(__name__)


@app.route('/books/review', methods=['POST'])
def review():
    payload = request.json
    return request.json


@app.route('/books/name/<bookname>')
def test_endpoint(bookname):
    return request_gutendex(bookname)


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


if __name__ == '__main__':
    app.run()

