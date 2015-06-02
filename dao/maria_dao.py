import MySQLdb as Mariadb


class MariaDao:
    """
        Base DAO class for MariaDB
    """

    timestamp_fmt = "%Y-%m-%d %H:%M:%S"

    def __init__(self, host, user, password, db):
        self._driver = Mariadb
        self._host = host
        self._user = user
        self._password = password
        self._db = db

    def _connect(self):
        con = self._driver.connect(self._host,
                                   self._user,
                                   self._password,
                                   self._db,
                                   charset='utf8',
                                   use_unicode=True)
        return con

    def _execute(self, sql):
        con = self._connect()
        with con:
            cursor = con.cursor()
            cursor.execute(sql)
