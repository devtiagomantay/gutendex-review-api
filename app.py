from flask import Flask
import requests

app = Flask(__name__)


@app.route('/books/name/<bookname>')
def test_endpoint(bookname):
    return request_gutendex(bookname)


def request_gutendex(bookname):
    uri = 'https://gutendex.com/books?search=' + bookname
    response = requests.get(uri)
    return response.json()


if __name__ == '__main__':
    app.run()

