import sqlite3
from config.config import config
from .LogUtil import logger_init

logger = logger_init('DB')

class Sqlite:
    def __init__(self,db_conf):
        self.db_URI = db_conf['uri']
        self.conn = sqlite3.connect(self.db_URI)
        self.conn.row_factory = sqlite3.Row     #https://docs.python.org/3/library/sqlite3.html#sqlite3-howto-row-factory
        self.cursor = self.conn.cursor()
    def fetchone(self,sql):
        self.cursor.execute(sql)
        values = self.cursor.fetchone()
        return dict(values)
    def fetchall(self,sql):
        self.cursor.execute(sql)
        values = self.cursor.fetchall()
        return [dict(v) for v in values]

    def excute(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            logger.error("DB error: %s" % e)
            return False

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()


db = Sqlite(config.db)
# one = db.fetchone("select * from user_user")
# all = db.fetchall("select * from user_user")
# two = db.excute("update user_user set last_name='lv' where id=3")
# print(one)
# print(all)
# print(two)
