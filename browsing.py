import os

from dao.save_result_dao import SaveResultDao
from dao.browsing_maria_dao import BrowsingMariaDao
from browsing_reconstruct import BrowsingReconstruct

user = os.environ['MARIADB_ID']
password = os.environ['MARIADB_PASS']
browsing_dao = BrowsingMariaDao('localhost', user, password, 'interop2015')
browsing_reconstruct = BrowsingReconstruct(browsing_dao)
save_result_dao = SaveResultDao('/home/interop/2015/prod/browsing_history/wide.sqlite3')

for result in save_result_dao.get_result():
    browsing_reconstruct.add_http_result(result)
