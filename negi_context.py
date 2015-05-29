import os
import argparse
import configparser

from dao.browsing_dao import BrowsingDao
from dao.browsing_maria_dao import BrowsingMariaDao
from dao.word_maria_dao import WordMariaDao
from dao.negi_meta_maria_dao import NegiMetaMariaDao
from flask import Blueprint, Flask
from flask.ext.cors import CORS

description="""\
negi context for rest server
"""

browsing_db = '/tmp/browsing_history.sqlite3'

parser = argparse.ArgumentParser(description=description)
parser.add_argument('conf',\
                    type=str,\
                    help='directory path to config file')
args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.conf)

class NegiContext:
    config = config

    daos = dict(
            browsing=BrowsingDao(browsing_db),
            browsing_maria=BrowsingMariaDao(config['db']['host'],
                                            config['db']['user'],
                                            config['db']['password'],
                                            config['db']['database']),
            word=WordMariaDao(config['db']['host'],
                              config['db']['user'],
                              config['db']['password'],
                              config['db']['database']),
            negi_meta=NegiMetaMariaDao(config['db']['host'],
                                       config['db']['user'],
                                       config['db']['password'],
                                       config['db']['database']),
            )


def start():
    from api import v1
    app = Flask(__name__)
    cors = CORS(app)
    app.register_blueprint(v1, url_prefix='/v1')
    app.run(port=24001, debug=True)

if __name__ == "__main__":
    start()
