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
