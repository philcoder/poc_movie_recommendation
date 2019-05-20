from datetime import datetime
from app import db

#
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    username = db.Column(db.String(15), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    userrole = db.Column(db.String(5))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bodytext = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.bodytext)