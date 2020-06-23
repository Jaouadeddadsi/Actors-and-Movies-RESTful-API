# Actors-and-Movies-RESTful-API

This project is a part of Fullstack Nanodegree with [Udacity](https://www.udacity.com/). It is an API to manage movies and actors data.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## API Specifications

### Models:

    - Movies with attributes title and release date
    - Actors with attributes name, age and gender and many to many relationship with Movies

### Endpoints:

    - GET /actors and /movies
    - DELETE /actors/ and /movies/
    - POST /actors and /movies and
    - PATCH /actors/ and /movies/

### Roles:

    - Casting Assistant:
    	- Can view actors and movies
    - Casting Director:
     	- All permissions a Casting Assistant has and…
    	- Add or delete an actor from the database
    	- Modify actors or movies
    - Executive Producer:
    	- All permissions a Casting Director has and…
    	- Add or delete a movie from the database

## Getting started

### Pre-requisites and Local Development

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

From the backend folder run `pip install -r requirements.txt`. All required packages are included in the `requirements.txt` file.

##### Key Dependencies

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle a [postgresql](https://www.postgresql.org/) database.
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests.

#### Environment variables

    To setup environment variables run:
    ```shell
        source setup.sh
    ```

#### Running the server

To run the application locally, create a database, change the `database_path` in `models.py` and run the following commands:

```shell
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/).

The application is run on http://127.0.0.1:5000/ by default.

To run the app using [gunicorn](https://gunicorn.org/) run the following command:

```shell
    gunicorn wsgi:app
```

## API Reference

### Getting Started

#### deployement

The app was deployed to [Heroku](https://www.heroku.com/)

- Base URL: https://jaouad-capstone.herokuapp.com/

#### Authentication

The app uses [auth0](https://auth0.com/) for authentication to get **ACCESS_TOKEN** follow the following steps:

        - login page : https://jdlearn.us.auth0.com/authorize?audience=capstoneApi&response_type=token&client_id=EG5HLKUAzXcQr3q4LDUKvYa481SsY6s5&redirect_uri=https://jaouad-capstone.herokuapp.com/actors

- Authentication: The app uses [auth0](https://auth0.auth0.com/) for authentication to get access tokens uses one of the following credentials:
  - **Casting Assistant**: `email`: casting.assistant@gmail.com and `password`: capstoneApp2020
  - **Casting Director** : `email`: casting.director@gmail.com and `password`: capstoneApp2020
  - **Executive Producer** : `email`: executive.producer@gmail.com and `password`:capstoneApp2020

### Error Handling

Errors are returned as JSON objects in the following format:

```python
{
	"success": False,
	"code": "bad request",
	"description": "something missing in your request"
}
```

The API will return three six types when requests fail:

- 400: Bad Request.
- 401: Unauthorized.
- 403: Forbidden.
- 404: Resource not found.
- 422: Unprocessable.
- 405: Method Not Allowed.

### Endpoint Library

#### GET /actors

- General:

      	- Returns success value, and a list of actors data

- Sample: curl -H "Authorization: Bearer <ACCESS_TOKEN>" https://jaouad-capstone.herokuapp.com/actors

```python
{
    "actors": [
        {
            "id": 1,
            "name": "Actor 1",
            "age": 43,
            "gender": "M",
            "movies": [
                {
                    "id": 1,
                    "title": "Movie 1",
                    "release date": "Mon, 09 Mar 2015 00:00:00 GMT",
                },
                {
                    "id": 2,
                    "title": "Movie 2",
                    "release date": "Mon, 02 Mar 2020 00:00:00 GMT",
                }

            ]
        },
        {
            "id": 2,
            "name": "Actor 2",
            "age": 32,
            "gender": "F",
            "movies": [
                {
                    "id": 1,
                    "title": "Movie 1",
                    "release date": "Mon, 09 Mar 2015 00:00:00 GMT",
                }
            ]
        }
    ],
    "success": True
}

```

#### GET /movies

- General:

      	- Returns success value, and a list of movies data

- Sample: curl -H "Authorization: Bearer <ACCESS_TOKEN>" https://jaouad-capstone.herokuapp.com/movies

```python
{
    "movies": [
        {
            "id": 1,
            "title": "Movie 1",
            "release date": "Mon, 09 Mar 2015 00:00:00 GMT",
            "actors": [
                {
                    "id": 1,
                    "name": "Actor 1",
                    "age": 43,
                    "gender": "M"
                },
                {
                    "id": 2,
                    "name": "Actor 2",
                    "age": 32,
                    "gender": "F"
                }
            ]
        },
        {
            "id": 2,
            "title": "Movie 2",
            "release date": "Mon, 02 Mar 2020 00:00:00 GMT",
            "actors": [
                {
                    "id": 1,
                    "name": "Actor 1",
                    "age": 43,
                    "gender": "M"
                }
            ]
        }
    ],
    "success": True
}
```

#### POST /actors

- General:

      	- Add a new actor to the actor's table

- Sample: curl -X POST https://jaouad-capstone.herokuapp.com/actors -H "Authorization: Bearer <ACCESS_TOKEN>, Content-Type: application/json" -d '{"name": "Actor 3", "age": 23, "gender": "F", "movies": []}'

```python
{
    "actors": [
        {
            "id": 3,
            "name": "Actor 2",
            "age": 23,
            "gender": "F",
            "movies": []
        }
    ],
    "success": True
}
```

#### POST /movies

- General:

      	- Add a new movie to the movie's table

- Sample: curl -X POST https://jaouad-capstone.herokuapp.com/movies -H "Authorization: Bearer <ACCESS_TOKEN>, Content-Type: application/json" -d '{"title": "Movie 3", "release_date": "2020-06-19", "actors": []}'

```python
{
    "movies": [
        {
            "id": 3,
            "title": "Movie 3",
            "release date":"Fri, 06 Jun 2020 00:00:00 GMT",
            "actors": []
        }
    ],
    "success": True
}
```

#### PATCH /actors/<int:actor_id>

- General:

      	- Update an actor data and we can use it to add movies to the actor movies list.
        - Return the actor data and success value equal True.

- Sample: curl -X PATCH https://jaouad-capstone.herokuapp.com/actor/1 -H "Authorization: Bearer <ACCESS_TOKEN>, Content-Type: application/json" -d '{"age": 56}'

```python
{
    "actors": [
        {
            "id": 1,
            "name": "Actor 1",
            "age": 56,
            "gender": "M",
            "movies": [
                {
                    "id": 1,
                    "title": "Movie 1",
                    "release date": "Mon, 09 Mar 2015 00:00:00 GMT",
                },
                {
                    "id": 2,
                    "title": "Movie 2",
                    "release date": "Mon, 02 Mar 2020 00:00:00 GMT",
                }

            ]
        }
    ],
    "success": True
}

```

#### PATCH /movies/<int:movie_id>

- General:

        - Update a movie data and we can use it to add actors to the movie actors list.
        - Return the movie data and success value equal True.

- Sample: curl -X PATCH https://jaouad-capstone.herokuapp.com/movies/1 -H "Authorization: Bearer <ACCESS_TOKEN>, Content-Type: application/json" -d '{"title": "Movie one"}'

```python
{
    "movies": [
        {
            "id": 1,
            "title": "Movie one",
            "release date": "Mon, 09 Mar 2015 00:00:00 GMT",
            "actors": [
                {
                    "id": 1,
                    "name": "Actor 1",
                    "age": 56,
                    "gender": "M"
                },
                {
                    "id": 2,
                    "name": "Actor 2",
                    "age": 32,
                    "gender": "F"
                }
            ]
        }
    ],
    "success": True
}
```

#### DELETE /actors/<actor_id>

- General:

      	- Delete an actor by id
        - Return the deleted actor id and success value equal True

- Sample: curl -X DELETE https://jaouad-capstone.herokuapp.com/actors/1 -H "Authorization: Bearer <ACCESS_TOKEN>"

```python
{
    "delete": 1,
    "success": True
}
```

#### DELETE /movies/<int:movie_id>

- General:

        - Delete a movie by id
        - Return the deleted movie id and success value equal True

- Sample: curl -X DELETE https://jaouad-capstone.herokuapp.com/movies/1 -H "Authorization: Bearer <ACCESS_TOKEN>"

```python
{
    "delete": 1,
    "success": True
}
```

### Tests

Before running tests refresh the access tokens in `access_token.py` file using the credentials giving above.

In order to run tests run the following commands:

```shell
source setup.sh
dropdb capstonedb_test
createdb capstonedb_test
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept `test_flaskr.py` file and should be maintained as updates are made to app functionality.

# Author

    Jaouad Eddadsi

# Acknowledgments

Many thanks to [Udacity](https://www.udacity.com/) for this amazing scholarship.
