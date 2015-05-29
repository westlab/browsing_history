import os
import argparse
import configparser

from dao.browsing_maria_dao import BrowsingMariaDao

description = """\
calcurate browsing time
"""

# TODO: remove this duplicated code in browsing.py
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

dao = BrowsingMariaDao(conf['host'],
                                conf['user'],
                                conf['password'],
                                conf['db'])

http_map = {}
for e in dao.get_id_srcip_timestamp():
    if e['src_ip'] in http_map:
        http = http_map[e['src_ip']]
        br_time = e['timestamp'] - http['timestamp']
        dao.update_browsint_time(http['id'], br_time.total_seconds())
    http_map[e['src_ip']] = e
