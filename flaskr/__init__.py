from flask import Flask
from models import setup_db, Movie, Actor
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(reponse):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    return app
