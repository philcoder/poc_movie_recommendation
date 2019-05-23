from app import db

from app.models import User, Movie

class UserDao():
    def add(self, name, username, password, userrole='user'):
        user = User(name=name, username=username, userrole=userrole)
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()

    def addAll(self, users):
        try:
            for user in users:
                db.session.add(user)

            db.session.commit()
        except Exception as e: 
            print(e)
            db.session.rollback() 

    def getUserByUsername(self, username):
        return User.query.filter_by(username=username).first()

    def getUserById(self, id):
        return User.query.get(id)

    def count(self):
        return User.query.count()        


class MovieDao():
    def add(self, movie):
        try:
            db.session.add(movie)
            db.session.commit()
        except Exception as e: 
            print(e)
            db.session.rollback()
    
    def addAll(self, movies):
        try:
            for movie in movies:
                db.session.add(movie)

            db.session.commit()
        except Exception as e: 
            print(e)
            db.session.rollback() 

    def count(self):
        return Movie.query.count()

    def deleteAll(self):
        try:
            num_rows_deleted = db.session.query(Movie).delete()
            db.session.commit()
            return num_rows_deleted
        except Exception as e:
            print(e)
            db.session.rollback()
            return -1

    def getMovieByName(self, name):
        sql = "%{}%".format(name)
        return Movie.query.filter(Movie.title.like(sql)).all()
    
    def getMovieById(self, id):
        return Movie.query.get(id)

class UserRating():
    def add(self, userRating):
        try:
            db.session.add(userRating)
            db.session.commit()
        except Exception as e: 
            print(e)
            db.session.rollback()

    def listAll(self):
        print("list all UR")    