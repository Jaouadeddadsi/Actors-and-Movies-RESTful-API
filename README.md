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
