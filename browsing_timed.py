from multiprocessing import Process
import time

from common.logging.logger_factory import LoggerFactory

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

def estimate_browsing_time(context):
    browsing_dao = context.daos['browsing_maria']
    meta_dao = context.daos['negi_meta']

    while True:
        http_map = {}
        for row in browsing_dao.get_id_srcip_timestamp():
            if row['src_ip'] in http_map:
                http = http_map[row['src_ip']]
                br_time = row['timestamp'] - http['timestamp']
                browsing_dao.update_browsint_time(http['id'], br_time.total_seconds())
        http_map[row['src_ip']] = row
        time.sleep(5)
        meta_dao.put('browsing_last_read_id', row['id'])

class BrowsingTimeWorker(Process):
    def __init__(self, context):
        #self._logger = LoggerFactory.create_logger("browsing_time_worker")
        self._context = context
        super().__init__()
        print("finish init")

    def run(self):
        print('hoge')
        #self._logger.info('BrowsingTimeWorker is instantiated.')
        browsing_dao = self._context.daos['browsing_maria']
        meta_dao = self._context.daos['negi_meta']

        while True:
            http_map = {}
            cnt = 0
            print('loop')
            row = None
            for row in browsing_dao.get_id_srcip_timestamp():
                print(row)
                cnt += 1
                if row['src_ip'] in http_map:
                    http = http_map[row['src_ip']]
                    br_time = row['timestamp'] - http['timestamp']
                    browsing_dao.update_browsint_time(http['id'], br_time.total_seconds())
                http_map[row['src_ip']] = row
        #    self._logger.info(str(cnt) + " are processed")
            if row:
                meta_dao.put('browsing_last_read_id', row['id'])
            time.sleep(5)
