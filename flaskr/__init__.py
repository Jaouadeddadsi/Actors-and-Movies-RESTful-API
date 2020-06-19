from flask import Flask, jsonify, abort, request
from models import setup_db, Movie, Actor
from flask_cors import CORS
from auth import requires_auth, AuthError


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
    @requires_auth('get:movies')
    def get_actors(payload):
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
    @requires_auth('get:movies')
    def get_movies(payload):
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
    @requires_auth('post:actors')
    def add_actor(payload):
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

        # create a new actor
        actor = Actor(name=name, age=age, gender=gender)
        # add movies
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

    '''
    POST /movies
        - it should create a new row in the movies table
        - it should require the 'post:movies' permission
        - it should contain the movie.long() data representation
        - returns status code 200 and json {"success": True, "actors": movie}
          where movie an array containing only the newly created movie or
          appropriate status code indicating reason for failure
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        # get the request body
        body = request.get_json()
        if body is None:
            abort(400)
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        actors = body.get('actors', None)

        # check title and release_date
        if (title is None) | (release_date is None):
            abort(400)
        # check if the movie already exist
        movie_old = Movie.query.filter_by(title=title).all()
        if len(movie_old) != 0:
            abort(409)

        # create a new movie
        movie = Movie(title=title, release_date=release_date)
        # add actors
        if len(actors) > 0:
            for actor in actors:
                name = actor.get('name', None)
                age = actor.get('age', None)
                gender = actor.get('gender', None)
                if (name is not None) and (age is not None):
                    # check if the actor already exist in the db
                    actor_row = Actor.query.filter_by(
                        name=name).one_or_none()
                    if actor_row:
                        movie.actors.append(actor_row)
                    else:
                        actor_row = Actor(
                            name=name, age=age, gender=gender)
                        movie.actors.append(actor_row)
        try:
            movie.insert()
            new_movie = Movie.query.get(movie.id)
            return jsonify({
                'success': True,
                'actors': [new_movie.long()]
            })
        except:
            abort(422)

    '''
    PATCH /actors/<id>
        - where <id> is the existing actor id
        - it should respond with a 404 error if <id> is not found
        - it should update the corresponding row for <id>
        - it should require the 'patch:actors' permission
        - it should contain the actor.long() data representation
        - returns status code 200 and json {"success": True, "actors": actor}
          where actor an array containing only the updated actor
          or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(actor_id, payload):
        # search the actor in the database
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)
        # get the request body
        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movies = body.get('movies', None)
        # update the name
        if name:
            actor.name = name
        # update the age
        if age:
            actor.age = age
        # update the gender
        if gender:
            actor.gender = gender
        # add new movies
        if movies:
            # get the existing movies titles
            movies_titles = [m.title for m in actor.movies]
            for movie in movies:
                if movie['title'] not in movies_titles:
                    # check if the movie already exist in the db
                    movie_row = Movie.query.filter_by(
                        title=movie['title']).one_or_none()
                    if movie_row:
                        actor.movies.append(movie_row)
                    else:
                        movie_new = Movie(title=movie['title'],
                                          release_date=movie['release_date'])
                        actor.movies.append(movie_new)
        try:
            actor.update()
            updated_actor = Actor.query.get(actor_id)
            return jsonify({
                'success': True,
                'actors': [updated_actor.long()]
            })
        except:
            abort(422)
    '''
    PATCH /movies/<id>
        - where <id> is the existing movie id
        - it should respond with a 404 error if <id> is not found
        - it should update the corresponding row for <id>
        - it should require the 'patch:movies' permission
        - it should contain the movie.long() data representation
        - returns status code 200 and json {"success": True, "movies": movie}
          where movie an array containing only the updated movie
          or appropriate status code indicating reason for failure
    '''
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(movie_id, payload):
        # search the movie in the database
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)
        # get the request body
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        actors = body.get('actors', None)
        # update the title
        if title:
            movie.title = title
        # update the release_date
        if release_date:
            movie.release_date = release_date
        # add new actors
        if actors:
            # get the existing actors name
            actors_names = [a.name for a in movie.actors]
            for actor in actors:
                if actor['name'] not in actors_names:
                    # check if the actor already exist in the db
                    actor_row = Actor.query.filter_by(
                        name=actor['name']).one_or_none()
                    if actor_row:
                        movie.actors.append(actor_row)
                    else:
                        actor_new = Actor(name=actor['name'],
                                          age=actor['age'],
                                          gender=actor.get('gender', None))
                        movie.actors.append(actor_new)
        try:
            movie.update()
            updated_movie = Movie.query.get(movie_id)
            return jsonify({
                'success': True,
                'movies': [updated_movie.long()]
            })
        except:
            abort(422)

    '''
    DELETE /actors/<id>
        - where <id> is the existing model id
        - it should respond with a 404 error if <id> is not found
        - it should delete the corresponding row for <id>
        - it should require the 'delete:actors' permission
        - returns status code 200 and json {"success": True, "delete": id}
          where id is the id of the deleted record or appropriate status
          code indicating reason for failure
    '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(actor_id, payload):
        # search the actor by id
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)
        try:
            actor.delete()
            return jsonify({
                'success': True,
                'delete': actor_id
            })
        except:
            abort(422)

    '''
    DELETE /movies/<id>
        - where <id> is the existing model id
        - it should respond with a 404 error if <id> is not found
        - it should delete the corresponding row for <id>
        - it should require the 'delete:movies' permission
        - returns status code 200 and json {"success": True, "delete": id}
          where id is the id of the deleted record or appropriate status
          code indicating reason for failure
    '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(movie_id, payload):
        # search the movie in the db
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)
        try:
            movie.delete()
            return jsonify({
                'success': True,
                'delete': movie_id
            })
        except:
            abort(422)

    '''
     error handler for AuthError
    '''
    @app.errorhandler(AuthError)
    def handle_AuthError(error):
        error.error['success'] = False
        return jsonify(error.error), error.status_code
    '''
    error handler for 422
    '''
    @app.errorhandler(422)
    def handle_422(error):
        return jsonify({
            "success": False,
            "code": "unprocessable",
            "description": "there is a problem interacting with the database"
        }), 422
    '''
    error handler for 404
    '''
    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            "success": False,
            "code": "resource not found",
            "description": "the requester resource doesn't exist in the db"
        }), 404
    '''
    error handler for 400
    '''
    @app.errorhandler(400)
    def handle_400(error):
        return jsonify({
            "success": False,
            "code": "bad request",
            "description": "something missing in your request"
        }), 400

    return app
