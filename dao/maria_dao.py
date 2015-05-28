import MySQLdb as Mariadb


class MariaDao:
    """
        Base DAO class for MariaDB
    """

    timestamp_fmt = "%Y-%m-%d %H:%M:%S"

    def __init__(self, host, user, password, db):
        self._driver = Mariadb
        self._con = self._driver.connect(host,
                                         user,
                                         password,
                                         db,
                                         charset='utf8',
                                         use_unicode=True)
    def __del__(self):
        if self._con:
            self._con.close()

    def _init_db(self, sql):
        cursor = self._con.cursor()
        cursor.execute(sql)
        self._con.commit()

    def _execute(self, sql):
        cursor = self._con.cursor()
        cursor.execute(sql)
        self._con.commit()
