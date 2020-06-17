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
roles
'''
roles = db.Table('roles',
                 db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
                 db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'))

                 )

'''
Movie
'''


class Movie(db.Model):
    """Movies table"""
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False, index=True)
    release_date = db.Column(db.Date, nullable=False)
    actors = db.relationship('Actor',
                             secondary=roles,
                             backref=db.backref('movies', lazy='dynamic'),
                             lazy='dynamic')

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

    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'release date': self.release_date,
        }

    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'release date': self.release_date,
            'actors': list(map(Actor.short, self.actors.all()))
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

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': list(map(Movie.short, self.movies.all()))
        }
