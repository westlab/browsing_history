from datetime import datetime
import sqlite3
import re
import time


def parse_timestamp(timestamp):
    """
        Parse timestamp

        >>> parse_timestamp('2015-4-30 18:59:34')
        datetime.datetime(2015, 4, 30, 18, 59, 34)
    """
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")


def parse_result(result, pattern):
    if pattern == 'Host:':
        l = result.split("\r\n")
        if l:
            return l[0].strip()

    if pattern == 'GET':
        l = result.split("\r\n")
        if l:
            uri = l[0].strip()
            index = uri.find(' ')
            if index:
                return uri[:index]

    if pattern == 'Content-Type:':
        l = result.split("\r\n")
        if l:
            content_type = l[0].strip()
            m = re.search('(.*);', content_type)
            if m:
                return m.group(1)

    if pattern == '<title':
        l = result.split("\r\n")
        if not l:
            return result

        title = l[0].strip()
        m = re.search('>(.*)<?', title)
        if m:
            clean_title = m.group(1).strip()
            index = clean_title.find('<')
            if index != -1:
                return clean_title[:index]
            return clean_title
    return result


class HTTPResult:
    def __init__(self, id, stream_id, src_ip, src_port, dst_ip, dst_port, pattern, timestamp, result):
        self._id = id
        self._stream_id = stream_id
        self._src_ip = src_ip
        self._dst_ip = dst_ip
        self._src_port = src_port
        self._dst_port = dst_port
        self._pattern = pattern
        self._timestamp = parse_timestamp(timestamp)
        self._result = parse_result(result, pattern)

    @property
    def id(self):
        return self._id

    @property
    def stream_id(self):
        return self._stream_id

    @property
    def src_ip(self):
        return self._src_ip

    @property
    def src_port(self):
        return self._src_port

    @property
    def dst_ip(self):
        return self._dst_ip

    @property
    def dst_port(self):
        return self._dst_port

    @property
    def pattern(self):
        return self._pattern

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def result(self):
        return self._result

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.__dict__)


class SaveResultDao:
    def __init__(self, db):
        self._conn = sqlite3.connect(db)
        self._conn.text_factory = lambda x: x.decode('utf-8', errors='ignore')
        self._select_sql = ("SELECT id, stream_id, src_ip, src_port, dst_ip, dst_port, pattern, timestamp, result "
                            "FROM save_result")

    def get_result(self, after=None, limit=None):
        c = self._conn.cursor()
        sql = self._select_sql

        if after is not None:
            sql += ' WHERE id > %d' % after

        if limit is not None:
            sql += ' LIMIT %d' % limit

        for row in c.execute(sql):
            yield self._format_result(row)

    def _format_result(self, row):
        return HTTPResult(*row)

if __name__ == "__main__":
    save_result_dao = SaveResultDao('/Users/ken/west/negis/webhistory/dbname.sqlite3')
    for result in save_result_dao.get_result():
        print(result)
