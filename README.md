# Actors-and-Movies-RESTful-API

This project is a part of Fullstack Nanodegree with [Udacity](https://www.udacity.com/). It is a coffee shop menu app where:

- Public users can view drink names and graphics.
- The shop baristas can see the recipe information.
- The shop managers can create new drinks and edit existing drinks.

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

#### Running the server

To run the application run the following commands:

```shell
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/).

The application is run on http://127.0.0.1:5000/ by default.

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
- Authentication: The app uses auth0 for authentication.

### Error Handling

Errors are returned as JSON objects in the following format:

```python
{
	"success": False,
	"code": "bad request",
	"description": "something missing in your request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request.
- 401: Unauthorized.
- 403: Forbidden.
- 404: Resource not found.
- 422: Unprocessable.
- 405: Method Not Allowed.

### Endpoint Library

#### GET /actors

- General:

      	- Returns success value, and an list of actors

- Sample: curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/actors

```python
{
    "actors": [
        {
            "id": 1,
            "name": "actor 1",
            "age": 43,
            "gender": "M",
            "movies": [
                {
                    "id": 1,
                    "title": "movie 1",
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

      	- Returns success value, and an list of movies

- Sample: curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://127.0.0.1:5000/movies

```python
{
    "movies": [
        {
            "id": 1,
            "title": "movie 1",
            "release date": "Mon, 09 Mar 2015 00:00:00 GMT",
            "actors": [
                {
                    "id": 1,
                    "name": "actor 1",
                    "age": 43,
                    "gender": "M"
                }
            ]
        }
    ]
}
```

#### POST /actors

- General:

      	- Add a new actor to the actors table

- Sample: curl -X POST http://127.0.0.1:5000/actors -H "Authorization: Bearer <ACCESS_TOKEN>, Content-Type: application/json" -d '{"name": "actor 2", "age": 23, "gender": "F", "movies": []}'

```python
{
    "actors": [
        {
            "id": 2,
            "name": "actor 2",
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

      	- Add a new movie to the movies table

- Sample: curl -X POST http://127.0.0.1:5000/movies -H "Authorization: Bearer <ACCESS_TOKEN>, Content-Type: application/json" -d '{"title": "movie 2", "release_date": "2020-06-19", "actors": []}'

```python
{
    "movies": [
        {
            "id": 2,
            "title": "movie 2",
            "release date":"Fri, 06 Jun 2020 00:00:00 GMT",
            "actors": []
        }
    ],
    "success": True
}
```

#### PATCH /actors

- General:

      	- Update actor

- Sample: curl -X PATCH http://127.0.0.1:5000/actor/1 -H "Authorization: Bearer <ACCESS_TOKEN>, Content-Type: application/json" -d '{"age": 56}'

```python
{
    "actors": [
        {
            "id": 1,
            "name": "actor 1",
            "age": 56,
            "gender": "M",
            "movies": [
                {
                    "id": 1,
                    "title": "movie 1",
                    "release date": "Mon, 09 Mar 2015 00:00:00 GMT",
                }
            ]
        }
    ],
    "success": True
}

```

#### PATCH /movies

- General:

      	- Update movie

- Sample: curl -X PATCH http://127.0.0.1:5000/movies/1 -H "Authorization: Bearer <ACCESS_TOKEN>, Content-Type: application/json" -d '{"title": "movie one"}'

```python
{
    "movies": [
        {
            "id": 1,
            "title": "movie one",
            "release date": "Mon, 09 Mar 2015 00:00:00 GMT",
            "actors": [
                {
                    "id": 1,
                    "name": "actor 1",
                    "age": 56,
                    "gender": "M"
                }
            ]
        }
    ],
    "success": True
}
```

#### DELETE /actors/1

- General:

      	- delete an actor by id

- Sample: curl -X DELETE http://127.0.0.1:5000/actors/1 -H "Authorization: Bearer <ACCESS_TOKEN>"

```python
{
    "delete": 1,
    "success": True
}
```

#### DELETE /movies/1

- General:
  - delete a movie by id
- Sample: curl -X DELETE http://127.0.0.1:5000/movies/1 -H "Authorization: Bearer <ACCESS_TOKEN>"

```python
{
    "delete": 1,
    "success": True
}
```

### Tests

In order to run tests run the following commands:

```shell
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
