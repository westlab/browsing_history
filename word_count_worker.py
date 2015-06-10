from multiprocessing import Process
import time
import re

import MeCab

from common.logging.logger_factory import LoggerFactory

sep = '[!-/:-@[-`{-~、◞⤴○▿゚д◟。♡٩ωو°！？（）〈〉【】『』／≦＜＼≧＞≪≫《》∀〔〕━──\n¥〜∵∴́ ❤⇒→⇔\│←↑↓┃★☆「」・♪～〓◆◇■□▽△▲●〇▼◎．”“※♥́́́]'
pat_sep = re.compile(sep)

MECAB_MODE = 'mecabrc -u /home/interop/2015/wikipedia.dic'
tagger = MeCab.Tagger(MECAB_MODE)

def clean_up_data(data):
    removed_sep = [re.sub(pat_sep, ' ', e) for e in data]
    return removed_sep

def parse2word(text):
    """
        Return generator of word
    """
    clean_text = "".join(clean_up_data(text))
    for mecab in tagger.parse(clean_text).splitlines():
        wakati = mecab.split("\t")
        if len(wakati) == 2:
            word = wakati[0]
            word_type = wakati[1].split(',')[0]
            yield word, word_type


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
            browsings = browsing_dao.get_after(['id', 'title'], browsing_id)
            browsing = None
            for browsing in browsings:
                cnt += 1
                words = [(word, 1) for word, word_type in parse2word(browsing['title']) if word_type == '名詞']
                filtered_words = list(filter(lambda word: len(word[0]) > 1, words))
                if filtered_words:
                    word_dao.bulk_put(filtered_words)

            if browsing:
                negi_meta_dao.put(last_browsing_id_by_word, browsing['id'])
                self._logger.info("{0} browsing are processed".format(cnt))
