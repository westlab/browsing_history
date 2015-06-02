from multiprocessing import Process
import time

from common.logging.logger_factory import LoggerFactory


class BrowsingTimeWorker(Process):
    def __init__(self, context):
        self._logger = LoggerFactory.create_logger(self)
        self._context = context
        super().__init__()

    def run(self):
        self._logger.info('BrowsingTimeWorker is instantiated.')
        browsing_dao = self._context.daos['browsing_maria']
        meta_dao = self._context.daos['negi_meta']

        while True:
            http_map = {}
            all_cnt = 0
            process_cnt = 0
            row = None
            for row in browsing_dao.get_id_srcip_timestamp():
                all_cnt += 1
                if row['src_ip'] in http_map:
                    http = http_map[row['src_ip']]
                    br_time = row['timestamp'] - http['timestamp']
                    browsing_dao.update_browsint_time(http['id'],
                                                      br_time.total_seconds())
                    process_cnt += 1
                http_map[row['src_ip']] = row
            self._logger.info("{0}/{1} are processed".format(process_cnt, all_cnt))
            if row:
                meta_dao.put('browsing_last_read_id', row['id'])
            time.sleep(5)
