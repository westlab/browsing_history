import random
from datetime import datetime, timedelta
import time


INSERT="""\
INSERT INTO browsing_history
(src_ip, src_port, dst_ip, dst_port, timestamp, title, url, browsing_time)
VALUES (
    "{src_ip}", {src_port}, "{dst_ip}", {dst_port}, "{timestamp}",
    "{title}", "{url}", {browsing_time}
)
"""

def random_ip(k):
    rand_ip = "10.24.1." + str(random.randint(1, k))
    return rand_ip

def random_port():
    return random.randint(1024, 65535)

def random_time(k):
    now = datetime.now()
    rand_time = now - timedelta(minutes=random.randint(1, k))
    return rand_time

def random_title():
    title_condidate = ['foo', 'bar', 'baz', 'hoge', 'fuga']
    return random.choice(title_condidate)

def random_url():
    domain_candidate = ['west', 'east', 'south', 'north', 'foo',
            'bar', 'gaga', 'github',  'google', 'yahoo', 'msn',
            'facebook', 'twitter', 'mixi', 'stackoverflow']
    return "http://" + random.choice(domain_candidate) + ".com"

def insert_dummy_browsing(context, number=-1, sleep=1):
    dao = context.daos['browsing_maria']

    def insert_dummy(self, sql):
        self._execute(sql)

    dao.insert_dummy = insert_dummy

    cnt = 0
    while True:
        if number > 0:
            if cnt > number:
                exit(0)
        dummy_sql = INSERT.format(src_ip=random_ip(30), src_port=random_port(),
                                  dst_ip=random_ip(255), dst_port=80,
                                  timestamp=random_time(300), title=random_title(),
                                  url=random_url(), browsing_time=random.randint(1, 500))
        dao._execute(dummy_sql)
        time.sleep(sleep)
