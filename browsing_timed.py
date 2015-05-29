def browsing_timed(context):
    browsing_dao = context.daos['browsing_maria']
    meta_dao = context.daos['negi_meta']

    http_map = {}
    for e in browsing_dao.get_id_srcip_timestamp():
        if e['src_ip'] in http_map:
            http = http_map[e['src_ip']]
            br_time = e['timestamp'] - http['timestamp']
            browsing_dao.update_browsint_time(http['id'], br_time.total_seconds())
        http_map[e['src_ip']] = e
    meta_dao.put('browsing_last_read_id', e['id'])
