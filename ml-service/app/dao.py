import psycopg2

class Dao:
    connect_str = "dbname='poc_db' user='root' host='postgres-service' password='phil.poc.ia'"

    def __init__(self):
        self.connect()

    def connect(self):
        self.conn = psycopg2.connect(self.connect_str)

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

class RatingDao(Dao):
    def __init__(self):
        Dao.__init__(self)

    def getUserIdByRatingId(self, rating_id):
        cursor =  super().cursor()
        cursor.execute("""select user_id from public.user_rating where id = %s;""" % (rating_id))
        return cursor.fetchone()[0] #fetch one item inside tuple


    def getAllRatings(self):
        cursor =  super().cursor()
        cursor.execute("""select user_id, movie_id, rating, '982126156' as fake_timestamp from public.user_rating order by id;""")
        return cursor.fetchall()

    def getDistinctUserId(self):
        cursor =  super().cursor()
        cursor.execute("""select DISTINCT user_id from public.user_rating order by user_id;""")
        return cursor.fetchall()

class SeggestMovieDao(Dao):
    def __init__(self):
        Dao.__init__(self)

    def addOrUpdate(self, ratingId, selectMovieIds):
        #clean
        if self.count(ratingId) != 0:
            self.deleteFromRatingId(ratingId)

        #add
        cursor = super().cursor()
        for movieId in selectMovieIds:
            cursor.execute("""insert into public.suggest_movies (rating_id, movie_id) values (%s, %s)""" % (ratingId, movieId))
        super().commit()

    def count(self, ratingId):
        cursor =  super().cursor()
        cursor.execute("""select count(*) from public.suggest_movies where rating_id = %s;""" % (ratingId))
        return cursor.fetchone()[0]
    
    def deleteFromRatingId(self, ratingId):
        cursor =  super().cursor()
        cursor.execute("""delete from public.suggest_movies where rating_id = %s;""" % (ratingId))
        super().commit()


# class TestDao(object):
#     connect_str = "dbname='poc_db' user='root' host='postgres-service' password='phil.poc.ia'"

#     def __init__(self):
#         self.connect()

#     def connect(self):
#         self.conn = psycopg2.connect(self.connect_str)

#     def cursor(self):
#         return self.conn.cursor()

#     def close(self):
#         self.conn.close()

#     def insertDataOnForm(self, bodytext, userid):
#         cursor = self.cursor()
#         cursor.execute("""insert into public.post (bodytext, user_id) values ('%s', %d) RETURNING id""" % (bodytext, userid))
#         self.conn.commit()
#         return cursor.fetchone()[0] #return id