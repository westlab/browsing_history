import argparse
import configparser
import time
from multiprocessing import Queue

from dao.browsing_maria_dao import BrowsingMariaDao
from dao.word_maria_dao import WordMariaDao
from dao.save_result_dao import SaveResultDao
from dao.negi_meta_maria_dao import NegiMetaMariaDao
from common.logging.logger_factory import LoggerFactory
from browsing_time_worker import BrowsingTimeWorker
from negi_load_worker import NegiLoadWorker
from browsing_reconstruct_worker import BrowsingReconstructWorker
from browsing_dummy import insert_dummy_browsing

description="""\
negi context for rest server
"""

parser = argparse.ArgumentParser(description=description)
parser.add_argument('program',
                    type=str,
                    choices=('server', 'browsing_timed', 'loader', 'dummy'),
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
        save_result=SaveResultDao(config['negi']['db']),
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
                                   config['db']['database'])
        )

    queues = dict(
        negi_result=Queue()
    )

context = NegiContext()

def rest_server():
    from flask import Flask
    from flask.ext.cors import CORS
    from api import v1

    LoggerFactory.init()
    logger = LoggerFactory.create_logger('rest_server')
    port = context.config.getint('rest_server', 'port')
    debug = context.config.getboolean('rest_server', 'debug')

    app = Flask(__name__)
    CORS(app, expose_headers=['X-Data-Count'])
    app.register_blueprint(v1, url_prefix='/v1')
    logger.info("Rest server start")
    app.run(port=port, debug=debug)

def browsing_time_daemon():
    LoggerFactory.init(config_file="browsing_time_estimation.cfg")
    browsing_time_worker = BrowsingTimeWorker(context)
    browsing_time_worker.daemon = True
    browsing_time_worker.start()
    while True:
        if not browsing_time_worker.is_alive():
            exit(1)
        time.sleep(1)

def loader():
    LoggerFactory.init(config_file="loader.cfg")
    processes = [
        NegiLoadWorker(context),
        BrowsingReconstructWorker(context)
    ]

    for p in processes:
        p.daemon = True
        p.start()

    while True:
        for p in processes:
            if not p.is_alive():
                exit(1)
        time.sleep(1)

def dummy():
    insert_dummy_browsing(context, sleep=0.2)

if __name__ == "__main__":
    if args.program == 'server':
        rest_server()
    if args.program == 'browsing_timed':
        browsing_time_daemon()
    if args.program == 'loader':
        loader()
    if args.program == 'dummy':
        dummy()
