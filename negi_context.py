from browsing_dao import BrowsingDao
from flask import Blueprint, Flask

browsing_db = '/tmp/browsing_history.sqlite3'

class NegiContext:
    daos = dict(
            browsing=BrowsingDao(browsing_db)
            )


def start():
    from api import v1
    app = Flask(__name__)
    app.register_blueprint(v1, url_prefix='/v1')
    app.run()

if __name__ == "__main__":
    start()
