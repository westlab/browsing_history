from multiprocessing import Process
import time

from common.logging.logger_factory import LoggerFactory

def parse2word(text):
    """
        Return generator of word
    """
    pass


class WordCountWorker(Process):
    def __init__(self, context):
        self._context = context
        self._logger = LoggerFactory.create_logger(self)
        super().__init__()

    def run(self):
        last_browsing_id_by_word = 'last_browsing_id_by_word'
        self._logger.info('WordCountWorker start')
        browsing_dao = self._context.daos['browsing_maria']
        word_dao = self._context.daos['word']
        negi_meta_dao = self._context.daos['negi_meta']
        while True:
            cnt = 0
            browsing_id = negi_meta_dao.get(last_browsing_id_by_word)
            browsings = browsing_dao.get_after(['id', 'title'], int(browsing_id))
            browsing = None
            for browsing in browsings:
                cnt += 1
                words = [(word, 1) for word in parse2word(browsing['title'])]
                word_dao.bulk_put(words)

            if browsing:
                negi_meta_dao.put(last_browsing_id_by_word, browsing['id'])
                self._logger.info("{0} browsing are processed".format(cnt))
            time.sleep(5)
