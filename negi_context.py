import os
import argparse
import configparser

from dao.browsing_dao import BrowsingDao
from dao.browsing_maria_dao import BrowsingMariaDao
from dao.word_maria_dao import WordMariaDao
from dao.negi_meta_maria_dao import NegiMetaMariaDao
from common.logging.logger_factory import LoggerFactory

description="""\
negi context for rest server
"""

browsing_db = '/tmp/browsing_history.sqlite3'

parser = argparse.ArgumentParser(description=description)
parser.add_argument('program',
                    type=str,
                    choices=('server', 'browsing_timed'),
                    help='program that you want to run')
parser.add_argument('conf',
                    type=str,
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


def rest_server():
    from flask import Flask
    from flask.ext.cors import CORS
    from api import v1
    LoggerFactory.init()
    logger = LoggerFactory.create_logger('rest_server')
    logger.info("test")
    context = NegiContext
    port = context.config.getint('rest_server', 'port')
    debug = context.config.getboolean('rest_server', 'debug')

    app = Flask(__name__)
    cors = CORS(app)
    app.register_blueprint(v1, url_prefix='/v1')
    app.run(port=port, debug=debug)

def browsing_time_deamon():
    from browsing_timed import browsing_timed
    browsing_timed(NegiContext)

def load_from_negi():
    pass


if __name__ == "__main__":
    if args.program == 'server':
        rest_server()
    if args.program == 'browsing_timed':
        browsing_time_deamon()
