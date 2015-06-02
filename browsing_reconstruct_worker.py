from multiprocessing import Process

from browsing_reconstruct import BrowsingReconstruct
from common.logging.logger_factory import LoggerFactory

class BrowsingReconstructWorker(Process):
    def __init__(self, context):
        self._context = context
        self._logger = LoggerFactory.create_logger(self)
        super().__init__()

    def run(self):
        self._logger.info('BrowsingReconstructorWorker start')
        browsing_dao = self._context.daos['browsing_maria']
        negi_result_q = self._context.queues['negi_result']
        browsing_reconstruct = BrowsingReconstruct(browsing_dao)
        while True:
            result = negi_result_q.get()
            browsing_reconstruct.add_http_result(result)
