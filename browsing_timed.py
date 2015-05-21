from dao.browsing_dao import BrowsingDao


dao = BrowsingDao('/tmp/browsing_history.sqlite3')
http_map = {}
for e in dao.get_id_srcip_timestamp():
    if e['src_ip'] in http_map:
        http = http_map[e['src_ip']]
        br_time = e['timestamp'] - http['timestamp']
        dao.update_browsint_time(http['id'], br_time.total_seconds())
    http_map[e['src_ip']] = e
