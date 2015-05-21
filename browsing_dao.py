import sqlite3
import re
from datetime import datetime


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

SELECT_FOR_BROWSING_TIME = """\
SELECT id, src_ip, timestamp FROM browsing_history
WHERE browsing_time IS NULL OR browsing_time = ''
"""

UPDATE_BROWSING_TIME="""\
UPDATE browsing_history
SET browsing_time = '{browsing_time}'
WHERE id = {id}
"""

SELECT_TMP = """\
SELECT {cols} FROM browsing_history
WHERE browsing_time IS NOT NULL
ORDER BY id DESC
LIMIT {limit}
"""

SELECT_WHERE = """\
SELECT {cols} FROM browsing_history
WHERE browsing_time IS NOT NULL AND {condition}
ORDER BY id DESC
LIMIT {limit}
"""

COUNT = """\
SELECT COUNT(*) FROM browsing_history
WHERE browsing_time IS NOT NULL
"""

COUNT_WHERE = """\
SELECT COUNT(*) FROM browsing_history
WHERE browsing_time IS NOT NULL AND {condition}
"""


timestamp_tmp = "%Y-%m-%d %H:%M:%S"

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

    def get_id_srcip_timestamp(self):
        sql = SELECT_FOR_BROWSING_TIME
        for row in self._conn.execute(sql):
            yield dict(id=row[0], src_ip=row[1],
                        timestamp=datetime.strptime(row[2], timestamp_tmp))

    def update_browsint_time(self, http_id, browsing_time):
        sql = UPDATE_BROWSING_TIME.format(id=http_id,
                                          browsing_time=browsing_time)
        self._conn.execute(sql)
        self._conn.commit()

    def get_with_browsing_time(self, cols, limit=100):
        sql = SELECT_TMP.format(cols=",".join(cols), limit=limit)
        for row in self._conn.execute(sql):
            yield dict(zip(cols, row))

    def get_browsing_by_src_ip(self, src_ip, cols, limit=100):
        condition = "src_ip = '%s'" % src_ip
        sql = SELECT_WHERE.format(cols=",".join(cols), limit=limit, condition=condition)
        for row in self._conn.execute(sql):
            yield dict(zip(cols, row))

    def count_all(self):
        sql = COUNT
        r = self._conn.execute(sql).fetchone()
        return r[0]

    def count_all_with_condition(self, condition):
        sql = COUNT_WHERE.format(condition=condition)
        r = self._conn.execute(sql).fetchone()
        return r[0]



if __name__ == "__main__":
    bd = BrowsingDao('/tmp/browsing_history.sqlite3')
#    r = bd.get_browsing_by_src_ip('172.16.79.11', ['id'])
#    print(list(r))
    print(bd.count_all())
