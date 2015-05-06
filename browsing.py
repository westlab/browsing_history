from save_result_dao import SaveResultDao
from browsing_reconstruct import BrowsingReconstruct

browsing_reconstruct = BrowsingReconstruct()
save_result_dao = SaveResultDao('/Users/ken/west/negis/webhistory/dbname.sqlite3')

for result in save_result_dao.get_result():
    browsing_reconstruct.add_http_result(result)
