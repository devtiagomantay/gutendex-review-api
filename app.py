from flask import Flask

app = Flask(__name__)


@app.route('/')
def test_endpoint():
 return 'It worked!'


if __name__ == '__main__':
 app.run()
