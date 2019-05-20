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
    password_hash = db.Column(db.String(128))
    userrole = db.Column(db.String(5))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bodytext = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.bodytext)

#for flask login library, loading the user from database using id
@login.user_loader
def load_user(id):
    return User.query.get(int(id))