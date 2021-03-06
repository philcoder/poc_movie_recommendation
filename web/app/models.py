from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db
from app import login

#
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    username = db.Column(db.String(15), index=True, unique=True)
    password_hash = db.Column('pw', db.String(128))
    userrole = db.Column(db.String(5))

    ratings = db.relationship('UserRating', backref='user_rating', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class UserRating(db.Model):
    __tablename__ = "user_rating"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    rating = db.Column(db.Integer)

    suggest_movies = db.relationship('SuggestMovies', backref='suggest_movies', lazy='dynamic') # lazy only be used with one-to-many
    movie = db.relationship('Movie', backref='user_rating_movie') # one-to-one

    def __repr__(self):
        return '<UserRating user_id={}, movie_id={} rating={}>'.format(self.user_id, self.movie_id, self.rating)

class SuggestMovies(db.Model):
    __tablename__ = "suggest_movies"
    id = db.Column(db.Integer, primary_key=True)
    rating_id = db.Column(db.Integer, db.ForeignKey('user_rating.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))

    movie = db.relationship('Movie', backref='suggest_movies_movie')

    def __repr__(self):
        return '<SuggestMovies rating_id={}, movie={}>'.format(self.rating_id, self.movie)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(90), index=True)
    release_date = db.Column(db.String(12))
    genres = db.Column(db.String(90))

    def __repr__(self):
        return '<Movie id:{}, title:{}>'.format(self.id, self.title)

#for flask login library, loading the user from database using id
@login.user_loader
def load_user(id):
    return User.query.get(int(id))