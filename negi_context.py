import os

from dao.browsing_dao import BrowsingDao
from dao.browsing_maria_dao import BrowsingMariaDao
from dao.negi_meta_maria_dao import NegiMetaMariaDao
from flask import Blueprint, Flask
from flask.ext.cors import CORS

browsing_db = '/tmp/browsing_history.sqlite3'
host = 'localhost'
user = os.environ['MARIADB_ID']
password = os.environ['MARIADB_PASS']
db = 'interop2015'

class NegiContext:
    daos = dict(
            browsing=BrowsingDao(browsing_db),
            browsing_maria=BrowsingMariaDao(host, user, password, db),
            word=WordMariaDao(host, user, password, db),
            negi_meta=NegiMetaMariaDao(host, user, password, db)
            )


def start():
    from api import v1
    app = Flask(__name__)
    cors = CORS(app)
    app.register_blueprint(v1, url_prefix='/v1')
    app.run(port=24001, debug=True)

if __name__ == "__main__":
    start()
