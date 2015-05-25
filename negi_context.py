import os

from dao.browsing_dao import BrowsingDao
from dao.browsing_maria_dao import BrowsingMariaDao
from flask import Blueprint, Flask

browsing_db = '/tmp/browsing_history.sqlite3'
host = 'localhost'
user = os.environ['MARIADB_ID']
password = os.environ['MARIADB_PASS']
db = 'interop2015'

class NegiContext:
    daos = dict(
            browsing=BrowsingDao(browsing_db),
            browsing_maria=BrowsingMariaDao(host,
                                            user,
                                            password,
                                            db)
            )


def start():
    from api import v1
    app = Flask(__name__)
    app.register_blueprint(v1, url_prefix='/v1')
    app.run(port=24001, debug=True)

if __name__ == "__main__":
    start()
