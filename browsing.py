from save_result_dao import SaveResultDao
from browsing_reconstruct import BrowsingReconstruct

browsing_reconstruct = BrowsingReconstruct('/tmp/browsing_history.sqlite3')
save_result_dao = SaveResultDao('/Users/ken/west/interop/webhistory/wide.sqlite3')

for result in save_result_dao.get_result():
    browsing_reconstruct.add_http_result(result)
