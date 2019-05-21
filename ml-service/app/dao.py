import psycopg2

class TestDao(object):
    connect_str = "dbname='poc_db' user='root' host='postgres-service' password='phil.poc.ia'"

    def __init__(self):
        self.connect()

    def connect(self):
        self.conn = psycopg2.connect(self.connect_str)

    def cursor(self):
        return self.conn.cursor()

    def close(self):
        self.conn.close()

    def insertDataOnForm(self, bodytext, userid):
        cursor = self.cursor()
        cursor.execute("""insert into public.post (bodytext, user_id) values ('%s', %d) RETURNING id""" % (bodytext, userid))
        self.conn.commit()
        return cursor.fetchone()[0] #return id