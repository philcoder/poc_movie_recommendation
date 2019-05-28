from app.util import Singleton

import psycopg2
from psycopg2 import pool

class DatabasePoolConnection(metaclass=Singleton):
    __instance = None
    __conn_pool = None

    def __init__(self):
        self._connect()
        if DatabasePoolConnection.__instance != None:
            raise Exception("This class is a DatabasePoolConnection!")
        else:
            DatabasePoolConnection.__instance = self

    def _connect(self):
        try:
            self.__conn_pool = psycopg2.pool.SimpleConnectionPool(1, 20,user = "root",
                                            password = "phil.poc.ia",
                                            host = "postgres-service",
                                            port = "5432",
                                            database = "poc_db")
        
            if(self.__conn_pool):
                print("Connection pool created successfully")
        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while connecting to PostgreSQL", error)

    def close(self):
        if (self.__conn_pool):
            self.__conn_pool.closeall

        print("PostgreSQL connection pool is closed")

    def getConnect(self):
        return self.__conn_pool.getconn()

    def putConnect(self, conn):
        self.__conn_pool.putconn(conn)

class Dao:
    __pool = None
    def __init__(self):
        self.__pool = DatabasePoolConnection()

    def getResult(self, sql):
        conn  = self.__pool.getConnect()
        if(conn):
            cursor = None
            try:
                cursor = conn.cursor()
                cursor.execute(sql)
                return cursor.fetchone()[0]
            except (Exception) as error :
                 print ("Error database: ", error)
            finally:
                cursor.close()
                self.__pool.putConnect(conn)

     
    def getResults(self, sql):
        conn  = self.__pool.getConnect()
        if(conn):
            cursor = None
            try:
                cursor = conn.cursor()
                cursor.execute(sql)
                return cursor.fetchall()
            except (Exception) as error :
                 print ("Error database: ", error)
            finally:
                cursor.close()
                self.__pool.putConnect(conn)

    def executeQuery(self, query):
        queries = []
        queries.append(query)
        self.executeQueries(queries)

    def executeQueries(self, queries):
        conn  = self.__pool.getConnect()
        if(conn):
            cursor = None
            try:
                cursor = conn.cursor()
                for query in queries:
                    cursor.execute(query)
            except (Exception) as error :
                 print ("Error database: ", error)
            finally:
                cursor.close()
                conn.commit()
                self.__pool.putConnect(conn)


class RatingDao(Dao):
    def __init__(self):
        Dao.__init__(self)

    def getUserIdByRatingId(self, rating_id):
        return super().getResult("""select user_id from public.user_rating where id = %s;""" % (rating_id))


    def getAllRatings(self):
        return super().getResults("""select user_id, movie_id, rating, '982126156' as fake_timestamp from public.user_rating order by id;""")

    def getDistinctUserId(self):
        return super().getResults("""select DISTINCT user_id from public.user_rating order by user_id;""")

class SuggestMovieDao(Dao):
    def __init__(self):
        Dao.__init__(self)

    def addOrUpdate(self, ratingId, selectMovieIds):
        #clean
        if self.count(ratingId) != 0:
            self.deleteFromRatingId(ratingId)

        queries = []
        for movieId in selectMovieIds:
            queries.append("""insert into public.suggest_movies (rating_id, movie_id) values (%s, %s)""" % (ratingId, movieId))
        super().executeQueries(queries)

    def count(self, ratingId):
        return super().getResult("""select count(*) from public.suggest_movies where rating_id = %s;""" % (ratingId))
    
    def deleteFromRatingId(self, ratingId):
        super().executeQuery("""delete from public.suggest_movies where rating_id = %s;""" % (ratingId))
