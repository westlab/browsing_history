from multiprocessing import Process

from common.logging.logger_factory import LoggerFactory

class NegiLoadWorker(Process):
    def __init__(self, context):
        self._logger = LoggerFactory.create_logger(self)
        self._context = context
        super().__init__()

    def run(self):
        self._logger.info('NegiLoaderWorker start')
        save_result_dao = self._context.daos['save_result']
        negi_meta = self._context.daos['negi_meta']
        negi_result_q = self._context.queues['negi_result']
        last_laod_id_key = 'negi_last_load_id'
        while True:
            result = None
            last_id = negi_meta.get(last_laod_id_key)
            for result in save_result_dao.get_result(after=last_id):
                negi_result_q.put(result)
            if result:
                negi_meta.put(last_laod_id_key, result.id)
                self._logger.info("last id: {0}".format(result.id))
