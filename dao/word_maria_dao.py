from collections import Counter
from datetime import datetime, timedelta

from maria_dao import MariaDao

INIT_WORD = """\
CREATE TABLE IF NOT EXISTS `word` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `count` int(11) DEFAULT 0,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `index_word_on_timestamp` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

WORD_WITHIN = """\
SELECT {cols} FROM word
WHERE timestamp > {border}
"""

WORD_INSERT = """\
INSERT INTO word (name, count)
VALUES
{words}
"""

def bulk_insert_sql(words):
    formated_word = ["('{0}', {1})".format(*w) for w in words]
    return WORD_INSERT.format(words=", ".join(formated_word))

class WordMariaDao(MariaDao):
    def __init__(self, host, user, password, db):
        super(MariaDao, self).__init__(host, user, password, db)
        self._init_db(INIT_WORD)

    def get(self, within, n=100):
        """
        Return top n word within x minites
        """
        cols = ['name', 'count']
        c = Counter()
        now = datetime.now()
        timestamp = now - timedelta(minutes = within)
        sql = WORD_WITHIN.format(
                    cols=",".join(cols),
                    border=timestamp.strftime(self.timestamp_fmt)
                )
        cursor = self._con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            c[row[0]] += row[1]
        top = c.most_common(n)
        r = [dict(name=x[0],count=x[1]) for x in top]
        return r

    def bulk_put(self, words):
        sql = bulk_insert_sql(words)
        self._execute(sql)

    def put(self, word, count):
        sql = WORD_INSERT.format(words="('{0}', {1})".format(word, count))
        self._execute(sql)
