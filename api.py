from flask import Blueprint, Response, json
from negi_context import NegiContext

v1 = Blueprint('v1', __name__)
browsing_dao = NegiContext.daos['browsing']

@v1.route('/browsings', methods=['GET'])
def browsings():
    cols = ['id', 'url', 'src_ip', 'dst_ip', 'timestamp', 'title', 'browsing_time']
    browsings = browsing_dao.get_with_browsing_time(cols)
    data = list(browsings)
    count = browsing_dao.count_all()
    headers = {"X-Data-Count": count}
    return Response(json.dumps(data),
                    mimetype='application/json',
                    headers=headers)

@v1.route('/browsings', methods=['HEAD'])
def browsing_count():
    count = browsing_dao.count_all()
    headers = {"X-Data-Count": count}
    return Response("", headers=headers)

@v1.route('/browsings/<src_ip>', methods=['GET'])
def personal_browsing(src_ip):
    cols = ['id', 'url', 'src_ip', 'dst_ip', 'timestamp', 'title', 'browsing_time']
    browsings = browsing_dao.get_browsing_by_src_ip(src_ip, cols)
    data = list(browsings)
    count = browsing_dao.count_all_with_condition("src_ip = '%s'" % src_ip)
    headers = {"X-Data-Count": count}
    return Response(json.dumps(data),
                    mimetype='application/json',
                    headers=headers)