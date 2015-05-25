import os

from dao.browsing_maria_dao import BrowsingMariaDao


user = os.environ['MARIADB_ID']
password = os.environ['MARIADB_PASS']
dao = BrowsingMariaDao('localhost', user, password, 'interop2015')

http_map = {}
for e in dao.get_id_srcip_timestamp():
    if e['src_ip'] in http_map:
        http = http_map[e['src_ip']]
        br_time = e['timestamp'] - http['timestamp']
        dao.update_browsint_time(http['id'], br_time.total_seconds())
    http_map[e['src_ip']] = e
