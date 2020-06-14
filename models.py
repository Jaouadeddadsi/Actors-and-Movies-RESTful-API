from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils.types.choice import ChoiceType

database_name = "capstonedb"
database_path = f'postgres:///{database_name}'

db = SQLAlchemy()
migrate = Migrate()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    """This function config the app with the database."""
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)


'''
Movie
'''


class Movie(db.Model):
    """Movies table"""
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False, index=True)
    release_date = db.Column(db.Date, nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'))

    def __repr__(self):
        return f'<Movie Title: {self.title}, Reale date: {self.release_date}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'title': self.title,
            'release date': self.release_date
        }


'''
Actor
'''


class Actor(db.Model):
    """Actors table"""
    __tablename__ = "actors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50))
    movies = db.relationship('Movie', backref='actor')

    def __repr__(self):
        return f'<Actor name: {self.name}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
