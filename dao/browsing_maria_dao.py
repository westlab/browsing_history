import re
from urllib.parse import urlparse
from datetime import datetime, timedelta
from collections import Counter

import MySQLdb as Mariadb

from dao.browsing_sql import *


timestamp_fmt = "%Y-%m-%d %H:%M:%S"

class BrowsingMariaDao:
    def __init__(self, host, user, password, db):
        self._driver = Mariadb
        self._con = self._driver.connect(host,
                                         user,
                                         password,
                                         db,
                                         charset='utf8',
                                         use_unicode=True)
        self._init_db()

    def __del__(self):
        if self._con:
            self._con.close()

    def _init_db(self):
        cursor = self._con.cursor()
        cursor.execute(INIT_Maria)
        self._con.commit()

    def save(self, http_comm):
        title = http_comm.title
        title = title.replace("'", "''", 10000)
        sql = INSERT_HTTP_COMMUNICATION.format(
                src_ip=http_comm.src_ip, src_port=http_comm.src_port,
                dst_ip=http_comm.dst_ip, dst_port=http_comm.dst_port,
                timestamp=http_comm.timestamp,
                title=self._escape_sql(http_comm.title),
                url=self._escape_sql(http_comm.url))
        cursor = self._con.cursor()
        cursor.execute(sql)
        self._con.commit()

    def _escape_sql(self, sql):
        sql = sql.replace("'", "''", 10000000)
        sql = sql.replace('"', "", 10000000)
        return sql

    def get_id_srcip_timestamp(self):
        sql = SELECT_FOR_BROWSING_TIME
        cursor = self._con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            yield dict(id=row[0], src_ip=row[1],
                        timestamp=row[2])

    def update_browsint_time(self, http_id, browsing_time):
        sql = UPDATE_BROWSING_TIME.format(id=http_id,
                                          browsing_time=browsing_time)
        cursor = self._con.cursor()
        cursor.execute(sql)
        self._con.commit()

    def get_with_browsing_time(self, cols, limit=100):
        sql = SELECT_TMP.format(cols=",".join(cols), limit=limit)
        cursor = self._con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            yield dict(zip(cols, row))

    def get_browsing_by_src_ip(self, src_ip, cols, limit=100):
        condition = "src_ip = '%s'" % src_ip
        sql = SELECT_WHERE.format(cols=",".join(cols), limit=limit, condition=condition)
        cursor = self._con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            yield dict(zip(cols, row))

    def count_all(self):
        sql = COUNT
        cursor = self._con.cursor()
        cursor.execute(sql)
        r = cursor.fetchone()
        return r[0]

    def count_all_with_condition(self, condition):
        sql = COUNT_WHERE.format(condition=condition)
        cursor = self._con.cursor()
        cursor.execute(sql)
        r = cursor.fetchone()
        return r[0]

    def domain_ranking(self, n=10):
        c = Counter()
        sql = DOMAIN
        cursor = self._con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            if row[0]:
                o = urlparse(row[0])
                c[o.netloc] += 1
        top = c.most_common(n)
        r = [dict(name=x[0], count=x[1]) for x in top]
        return r

    def search(self, keyword, cols):
        sql = SEARCH_TMP.format(keyword=keyword, cols=",".join(cols))
        cursor = self._con.cursor()
        for row in cursor.execute(sql):
            yield dict(zip(cols, row))

    def src_ip_ranking(self, n=10):
        c = Counter()
        sql = SRCIP
        cursor = self._con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            c[row[0]] += 1
        top = c.most_common(n)
        r = [dict(name=x[0], count=x[1]) for x in top]
        return r

    def word_cloud(self, n=100):
        """
        Return word and word count within 30 minites
        """
        c = Counter()
        now = datetime.now()
        timestamp = now - timedelta(minutes = 30)
        sql = WORDCLOUD.format(border=timestamp.strftime(timestamp_fmt))
        cursor = self._con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            c[row[0]] += row[1]
        top = c.most_common(n)
        r = [dict(name=x[0],count=x[1]) for x in top]
        return r
