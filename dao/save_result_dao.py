import sqlite3
from dto.http_result_dto import HTTPResultDto

SELECT_SAVE_RESULT="""\
SELECT id, stream_id, src_ip, src_port, dst_ip, dst_port,
       pattern, timestamp, result
ROM save_result
"""

class SaveResultDao:
    def __init__(self, db):
        self._conn = sqlite3.connect(db)
        self._conn.text_factory = lambda x: x.decode('utf-8', errors='ignore')

    def get_result(self, after=None, limit=None):
        c = self._conn.cursor()
        sql = SELECT_SAVE_RESULT

        if after is not None:
            sql += ' WHERE id > %d' % after

        if limit is not None:
            sql += ' LIMIT %d' % limit

        for row in c.execute(sql):
            yield self._format_result(row)

    def _format_result(self, row):
        return HTTPResultDto(*row)

if __name__ == "__main__":
    save_result_dao = SaveResultDao('/Users/ken/west/negis/webhistory/dbname.sqlite3')
    for result in save_result_dao.get_result():
        print(result)
