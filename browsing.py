import os
import argparse
import configparser

from dao.save_result_dao import SaveResultDao
from dao.browsing_maria_dao import BrowsingMariaDao
from browsing_reconstruct import BrowsingReconstruct

# TODO: make python module to store config object

description = """\
Extract Browsing history from NEGI(https://github.com/westlab/negi)
"""

conf = dict()
negi_conf = dict()

parser = argparse.ArgumentParser(description=description)
parser.add_argument('conf',\
                    type=str,\
                    help='directory path to config file')
args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.conf)

conf['user']= config['db']['user']
conf['password']= config['db']['password']
conf['host']= config['db']['host']
conf['db']= config['db']['database']
negi_conf['db'] = config['negi']['db']

browsing_dao = BrowsingMariaDao(conf['host'],
                                conf['user'],
                                conf['password'],
                                conf['db'])
browsing_reconstruct = BrowsingReconstruct(browsing_dao)
save_result_dao = SaveResultDao(negi_conf['db'])

for result in save_result_dao.get_result():
    browsing_reconstruct.add_http_result(result)
