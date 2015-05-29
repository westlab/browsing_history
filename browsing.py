import os
import argparse
import configparser

from dao.save_result_dao import SaveResultDao
from dao.browsing_maria_dao import BrowsingMariaDao
from browsing_reconstruct import BrowsingReconstruct

description = """\
Extract Browsing history from NEGI(https://github.com/westlab/negi)
"""

parser = argparse.ArgumentParser(description=description)
parser.add_argument('-c', '--conf',\
                    type=str,\
                    help='directory path to config file')
args = parser.parse_args()
print(args)

config = configparser.ConfigParser()
config.read(args.conf)
print(config['negi']['db'])
exit(0)

user = os.environ['MARIADB_ID']
password = os.environ['MARIADB_PASS']
browsing_dao = BrowsingMariaDao('localhost', user, password, 'interop2015')
browsing_reconstruct = BrowsingReconstruct(browsing_dao)
save_result_db = os.environ['NEGI_SAVE_RESULT_DB']
save_result_dao = SaveResultDao(save_result_db)

for result in save_result_dao.get_result():
    browsing_reconstruct.add_http_result(result)
