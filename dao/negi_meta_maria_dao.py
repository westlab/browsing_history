from dao.maria_dao import MariaDao

INIT_NEGI_META="""\
CREATE TABLE IF NOT EXISTS `negi_meta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `value` text,
  PRIMARY KEY (`id`),
  UNIQUE `unique_negi_meta_on_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

INSERT_OR_UPDATE="""\
INSERT INTO negi_meta
  (name, value)
VALUES
  ('{name}', {value})
ON DUPLICATE KEY UPDATE
  value = VALUES(value)
"""

GET_VALUE="""\
SELECT value FROM negi_meta
WHERE name = {name}
LIMIT 1
"""

class NegiMetaMariaDao(MariaDao):
    def __init__(self, host, user, password, db):
        super().__init__(host, user, password, db)
        self._execute(INIT_NEGI_META)

    def put(self, key, val):
        sql = INSERT_OR_UPDATE.format(name=key, value=val)
        self._execute(sql)

    def get(self, key):
        sql = GET_VALUE.format(name=key)
        with self._con.cursor() as cursor:
            cursor.execute(sql)
            r = cursor.fetchone()
            if r:
                return r[0]
