import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# Load environment variables from .env file
load_dotenv()

database_uri = os.getenv('DATABASE_URI')

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_uri=database_uri):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()

"""
Movie

"""       
class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

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
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

"""
Movie

""" 
class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

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
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

def insertInitialData(app):
    # Insert some sample movies and  actors into the database
    movie1 = Movie(
        title='movie1',
        release_date='2010-07-16'
    )

    movie2 = Movie(
        title='movie2',
        release_date='1999-03-31'
    )

    movie3 = Movie(
        title='movie3',
        release_date='2014-11-07'
    )

    actor1 = Actor(
        name='actor 1',
        age=46,
        gender='Male'
    )

    actor2 = Actor(
        name='actor 2',
        age=57,
        gender='Male'
    )

    actor3 = Actor(
        name='actor 3',
        age=39,
        gender='Female'
    )

    with app.app_context():
        actor1.insert()
        actor2.insert()
        actor3.insert()
        movie1.insert()
        movie2.insert()
        movie3.insert()
