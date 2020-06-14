import unittest
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Movie, Actor, db
from test_data import actors


def populate_db(db, data=actors):
    """Write test data to the database"""
    for actor in data:
        actor_row = Actor(name=actor['name'], age=actor['age'],
                          gender=actor['gender'])
        for movie in actor['movies']:
            Movie(title=movie['title'],
                  release_date=movie['release_date'], actor=actor_row)
        actor_row.insert()


class AppTestCase(unittest.TestCase):
    """This class represents the models test cases"""

    def setUp(self):
        """Define test variables and initialise app."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "capstonedb_test"
        self.database_path = f'postgresql:///{self.database_name}'
        setup_db(self.app, self.database_path)
        with self.app.app_context():
            db.create_all()
            populate_db(db)

    def tearDown(self):
        """clear the database after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
