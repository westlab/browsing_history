import sqlite3
import re


INIT_SQL ="""\
CREATE TABLE IF NOT EXISTS "browsing_history" (
"id" INTEGER PRIMARY KEY AUTOINCREMENT,
"src_ip" TEXT,
"src_port" INTEGER,
"dst_ip" TEXT,
"dst_port" INTEGER,
"timestamp" TEXT,
"title" TEXT,
"url" TEXT,
"browsing_time" FLOAT
)
"""

INSERT_HTTP_COMMUNICATION = """\
INSERT INTO browsing_history
(src_ip, src_port, dst_ip, dst_port, timestamp, title, url)
VALUES
("{src_ip}", {src_port}, "{dst_ip}", {dst_port}, "{timestamp}", "{title}", "{url}")
"""



class BrowsingDao:
    def __init__(self, db):
        self._db = db
        self._conn = sqlite3.connect(self._db)
        self._conn.text_factory = lambda x: x.decode('utf-8', errors='ignore')
        self._init_db()

    def _init_db(self):
        self._conn.execute(INIT_SQL)
        self._conn.commit()

    def save(self, http_comm):
        title = http_comm.title
        title = title.replace("'", "''", 10000)
        sql = INSERT_HTTP_COMMUNICATION.format(
                src_ip=http_comm.src_ip, src_port=http_comm.src_port,
                dst_ip=http_comm.dst_ip, dst_port=http_comm.dst_port,
                timestamp=http_comm.timestamp,
                title=self._escape_sql(http_comm.title),
                url=self._escape_sql(http_comm.url))
        self._conn.execute(sql)
        self._conn.commit()

    def _escape_sql(self, sql):
        sql = sql.replace("'", "''", 10000000)
        sql = sql.replace('"', "", 10000000)
        return sql

    def calicurate_browsing_time(self):
        pass
