import time

from app.dao import TestDao

class Engine:

    def test(self, data):
        print(" [x] Received %r" % data)

        time.sleep(10)

        text = "You watch the {} at {}".format(data["type"], data["date"])
        dao = TestDao()
        dao.insertDataOnForm(text, int(data["userid"]))
        dao.close()
        print(" [x] Done")
