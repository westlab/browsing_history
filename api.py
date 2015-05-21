from flask import Blueprint, Response, json
from negi_context import NegiContext

v1 = Blueprint('v1', __name__)
browsing_dao = NegiContext.daos['browsing']

@v1.route('/browsings')
def browsings():
    cols = ['id', 'src_ip', 'dst_ip', 'timestamp', 'title', 'browsing_time']
    browsings = browsing_dao.get_with_browsing_time(cols)
    data = list(browsings)
    return Response(json.dumps(data),  mimetype='application/json')

@v1.route('/browsings/<src_ip>')
def personal_browsing(src_ip):
    cols = ['id', 'src_ip', 'dst_ip', 'timestamp', 'title', 'browsing_time']
    browsings = browsing_dao.get_browsing_by_src_ip(src_ip, cols)
    data = list(browsings)
    return Response(json.dumps(data),  mimetype='application/json')
