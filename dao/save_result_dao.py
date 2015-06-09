import sqlite3
from dto.http_result_dto import HTTPResultDto

SELECT_SAVE_RESULT="""\
SELECT id, stream_id, src_ip, src_port, dst_ip, dst_port,
       pattern, timestamp, result
FROM save_result
"""

class SaveResultDao:
    def __init__(self, db):
        self._db = db

    def _connect(self):
        con = sqlite3.connect(self._db)
        con.text_factory = lambda x: x.decode('utf-8', errors='ignore')
        return con

    def get_result(self, after=None, limit=None):
        sql = SELECT_SAVE_RESULT

        if after is not None:
            sql += ' WHERE id > {0}'.format(after)

        if limit is not None:
            sql += ' LIMIT {0}'.format(limit)

        con = self._connect()
        with con:
            cursor = con.cursor()
            cursor.execute(sql)
            for row in cursor.fetchall():
                yield self._format_result(row)

    def _format_result(self, row):
        return HTTPResultDto(*row)

if __name__ == "__main__":
    save_result_dao = SaveResultDao('/Users/ken/west/negis/webhistory/dbname.sqlite3')
    for result in save_result_dao.get_result():
        print(result)
