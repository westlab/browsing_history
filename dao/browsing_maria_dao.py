from urllib.parse import urlparse
from datetime import datetime, timedelta
from collections import Counter

from dao.maria_dao import MariaDao

from dao.browsing_sql import *


class BrowsingMariaDao(MariaDao):
    def __init__(self, host, user, password, db):
        super().__init__(host, user, password, db)
        self._execute(INIT_Maria)

    def save(self, http_comm):
        sql = INSERT_HTTP_COMMUNICATION.format(
            src_ip=http_comm.src_ip, src_port=http_comm.src_port,
            dst_ip=http_comm.dst_ip, dst_port=http_comm.dst_port,
            timestamp=http_comm.timestamp,
            title=self._escape_sql(http_comm.title),
            url=self._escape_sql(http_comm.url))
        self._execute(sql)

    def _escape_sql(self, sql):
        sql = sql.replace("'", "''", 10000000)
        sql = sql.replace('"', "", 10000000)
        return sql

    def get_id_srcip_timestamp(self, within=30):
        now = datetime.now()
        timeout = now - timedelta(minutes=within)
        sql = SELECT_FOR_BROWSING_TIME.format(timeout=timeout)
        con = self._connect()
        with con:
            cursor = con.cursor()
            cursor.execute(sql)
            for row in cursor.fetchall():
                yield dict(id=row[0], src_ip=row[1], timestamp=row[2])

    def update_browsint_time(self, http_id, browsing_time):
        sql = UPDATE_BROWSING_TIME.format(id=http_id,
                                          browsing_time=browsing_time)
        self._execute(sql)

    def get_with_browsing_time(self, cols, limit=100):
        sql = SELECT_TMP.format(cols=",".join(cols), limit=limit)
        con = self._connect()
        with con:
            cursor = con.cursor()
            cursor.execute(sql)
            for row in cursor.fetchall():
                yield dict(zip(cols, row))

    def get_browsing_by_src_ip(self, src_ip, cols, limit=100):
        condition = "src_ip = '%s'" % src_ip
        sql = SELECT_WHERE.format(cols=",".join(cols),
                                  limit=limit,
                                  condition=condition)
        con = self._connect()
        with con:
            cursor = con.cursor()
            cursor.execute(sql)
            for row in cursor.fetchall():
                yield dict(zip(cols, row))

    def count_all(self):
        sql = COUNT
        con = self._connect()
        with con:
            cursor = con.cursor()
            cursor.execute(sql)
            count = cursor.fetchone()[0]
            return count

    def count_all_with_condition(self, condition):
        sql = COUNT_WHERE.format(condition=condition)
        con = self._connect()
        with con:
            cursor = con.cursor()
            cursor.execute(sql)
            count = cursor.fetchone()[0]
            return count

    def domain_ranking(self, n=10):
        c = Counter()
        sql = DOMAIN
        con = self._connect()
        with con:
            cursor = con.cursor()
            cursor.execute(sql)
            for row in cursor.fetchall():
                if row[0]:
                    o = urlparse(row[0])
                    c[o.netloc] += 1
        top = c.most_common(n)
        domain_rank = [dict(name=x[0], count=x[1]) for x in top]
        return domain_rank

    def search(self, keyword, cols):
        sql = SEARCH_TMP.format(keyword=keyword, cols=",".join(cols))
        con = self._connect()
        with con:
            cursor = con.cursor()
            cursor.execute(sql)
            for row in cursor.fetchall():
                yield dict(zip(cols, row))

    def src_ip_ranking(self, n=10):
        c = Counter()
        sql = SRCIP
        con = self._connect()
        with con:
            cursor = con.cursor()
            cursor.execute(sql)
            for row in cursor.execute(sql):
                c[row[0]] += 1
        top = c.most_common(n)
        src_ip_rank = [dict(name=x[0], count=x[1]) for x in top]
        return src_ip_rank
