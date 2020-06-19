import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Movie, Actor, db
from test_data import actors
from access_token import tokens


def populate_db(db, data=actors):
    """Write test data to the database"""
    for actor in data:
        actor_row = Actor(name=actor['name'], age=actor['age'],
                          gender=actor['gender'])
        for movie in actor['movies']:
            # check if the movie existe in the db
            movie_row = Movie.query.filter_by(
                title=movie['title']).one_or_none()
            if movie_row is not None:
                actor_row.movies.append(movie_row)
            else:
                new_movie = Movie(title=movie['title'],
                                  release_date=movie['release_date'])
                actor_row.movies.append(new_movie)
        actor_row.insert()


# new data
new_actor = {
    'name': 'actor 3',
    'age': 34,
    'gender': 'F',
    'movies': [
        {
            'title': 'Movie 3',
            'release_date': '2009-06-03'
        },
        {
            'title': 'Movie 2',
            'release_date': '2020-01-08'
        }
    ]
}

new_movie = {
    'title': 'Movie 5',
    'release_date': '2010-06-23',
    'actors': [
        {
            'name': 'actor 2',
            'age': 50,
            'gender': 'F',
        },
        {
            'name': 'actor 4',
            'age': 45,
            'gender': 'M'
        }
    ]
}


class AppTestCase(unittest.TestCase):
    """This class represents the models test cases"""

    def setUp(self):
        """Define test variables and initialise app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "capstonedb_test"
        self.database_path = f'postgresql:///{self.database_name}'
        self.assistant = tokens['ASSISTANT']
        self.director = tokens['DIRECTOR']
        self.producer = tokens['PRODUCER']
        self.new_actor = new_actor
        self.new_movie = new_movie
        setup_db(self.app, self.database_path)
        with self.app.app_context():
            db.create_all()
            populate_db(db)

    def tearDown(self):
        """clear the database after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_actors_no_auth(self):
        res = self.client.get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'],
                         'Authorization header is expected')

    def test_get_actor_with_assistant(self):
        res = self.client.get('/actors',
                              headers={
                                  "Authorization": f'Bearer {self.assistant}'
                              })
        data = json.loads(res.data)
        actor = data['actors'][0]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 2)
        self.assertEqual(actor['name'], 'actor 1')
        self.assertEqual(actor['age'], 23)
        self.assertEqual(actor['gender'], 'M')
        self.assertEqual(len(actor['movies']), 2)

    def test_get_movies_no_auth(self):
        res = self.client.get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'],
                         'Authorization header is expected')

    def test_get_movies_with_assistant(self):
        res = self.client.get('/movies',
                              headers={
                                  "Authorization": f'Bearer {self.assistant}'
                              })
        data = json.loads(res.data)
        movie = data['movies'][0]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 4)
        self.assertEqual(movie['title'], 'Movie 1')
        self.assertIsNotNone(movie['release date'])

    def test_post_actor_with_assistant(self):
        res = self.client.post('/actors',
                               headers={
                                   "Authorization": f'Bearer {self.assistant}'
                               },
                               json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'],
                         'Permission not found.')

    def test_post_actor_with_director(self):
        res = self.client.post('/actors',
                               headers={
                                   "Authorization": f'Bearer {self.director}'
                               },
                               json=self.new_actor)
        data = json.loads(res.data)
        actor = data['actors'][0]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data['actors']), 1)
        self.assertEqual(actor['name'], 'actor 3')
        self.assertEqual(actor['age'], 34)
        self.assertEqual(actor['gender'], 'F')
        self.assertEqual(len(actor['movies']), 2)

    def test_patch_actor_with_director(self):
        res = self.client.patch('/actors/1',
                                headers={
                                    "Authorization": f'Bearer {self.director}'
                                },
                                json={'age': 25})
        data = json.loads(res.data)
        actor = data['actors'][0]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 1)
        self.assertEqual(actor['age'], 25)

    def test_patch_movie_with_director(self):
        res = self.client.patch('/movies/1',
                                headers={
                                    "Authorization": f'Bearer {self.director}'
                                },
                                json={'title': 'Movie number 1'})
        data = json.loads(res.data)
        movie = data['movies'][0]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)
        self.assertEqual(movie['title'], 'Movie number 1')

    def test_delete_actor_with_director(self):
        res = self.client.delete('/actors/1',
                                 headers={
                                     "Authorization": f'Bearer {self.director}'
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)

    def test_post_movie_with_producer(self):
        res = self.client.post('/movies',
                               headers={
                                   "Authorization": f'Bearer {self.producer}'
                               },
                               json=self.new_movie)
        data = json.loads(res.data)
        movie = data['movies'][0]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)
        self.assertEqual(movie['title'], 'Movie 5')
        self.assertIsNotNone(movie['release date'])
        self.assertEqual(len(movie['actors']), 2)

    def test_delete_movie_with_producer(self):
        res = self.client.delete('/movies/1',
                                 headers={
                                     "Authorization": f'Bearer {self.producer}'
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)


if __name__ == '__main__':
    unittest.main()
