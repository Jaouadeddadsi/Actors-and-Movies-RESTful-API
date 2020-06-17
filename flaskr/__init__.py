from flask import Flask, jsonify, abort, request
from models import setup_db, Movie, Actor
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    GET /actors
        - it is a public endpoint
        - it contain a list of actors data
        - return status code 200 and json {"success": True, "actors": actors}
          where actors is the list of actors or appropriate status code indicating
          reason for failure
    '''
    @app.route('/actors')
    def get_actors():
        try:
            # fetch list of actors ordered by id
            actors = list(
                map(Actor.long, Actor.query.order_by(Actor.id)))

            return jsonify({
                "success": True,
                "actors": actors
            })
        except:
            abort(422)

    '''
    GET /movies
        - it is a public endpoint
        - it contain a list of movies data
        - return status code 200 and json {"success": True, "movies": movies}
          where movies is the list of movies or apppropriate status code
          indicating reason for failure
    '''
    @app.route('/movies')
    def get_movies():
        try:
            # fetch the list of movies
            movies = list(map(Movie.long, Movie.query.order_by(Movie.id)))

            return jsonify({
                'success': True,
                'movies': movies
            })
        except:
            abort(422)

    '''
    POST /actors
        - it should create a new row in the actors table
        - it should require the 'post:actors' permission
        - it should contain the actor.long() data representation
        - returns status code 200 and json {"success": True, "actors": actor}
          where actor an array containing only the newly created actor or
          appropriate status code indicating reason for failure
    '''
    @app.route('/actors', methods=['POST'])
    def add_actor():
        # get the request body
        body = request.get_json()
        if body is None:
            abort(400)
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movies = body.get('movies', None)
        # check name and age
        if (name is None) | (age is None):
            abort(400)
        # check if the actor already exist
        actor_old = Actor.query.filter_by(name=name).all()
        if len(actor_old) != 0:
            abort(409)

        # build new actor
        actor = Actor(name=name, age=age, gender=gender)

        if len(movies) > 0:
            for movie in movies:
                title = movie.get('title', None)
                release_date = movie.get('release_date', None)
                if (title is not None) and (release_date is not None):
                    # check if the movie already exist in the db
                    movie_row = Movie.query.filter_by(
                        title=title).one_or_none()
                    if movie_row:
                        actor.movies.append(movie_row)
                        print(movie_row.title)
                    else:
                        movie_row = Movie(
                            title=title, release_date=release_date)
                        actor.movies.append(movie_row)
        try:
            actor.insert()
            new_actor = Actor.query.get(actor.id)
            return jsonify({
                'success': True,
                'actors': [new_actor.long()]
            })
        except:
            abort(422)

    return app
