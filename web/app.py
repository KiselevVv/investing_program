import os

from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(10)


@app.route('/', methods=['GET'])
def index_page():
    return 'Hello'


if __name__ == '__main__':
    app.run()
