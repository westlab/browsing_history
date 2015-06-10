from flask import Blueprint, Response, json, request

from negi_context import context

v1 = Blueprint('v1', __name__)
browsing_dao = context.daos['browsing_maria']
word_dao = context.daos['word']
cols = ['id', 'url', 'src_ip', 'dst_ip', 'timestamp', 'title', 'browsing_time']

@v1.route('/browsings', methods=['GET'])
def get_browsings():
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
    browsings = browsing_dao.get_browsing_by_src_ip(src_ip, cols)
    data = list(browsings)
    count = browsing_dao.count_all_with_condition("src_ip = '%s'" % src_ip)
    headers = {"X-Data-Count": count}
    return Response(json.dumps(data),
                    mimetype='application/json',
                    headers=headers)

@v1.route('/rankings/domain', methods=['GET'])
def domain_ranking():
    limit = request.args.get('limit', default=10, type=int)
    within = request.args.get('within', default=30, type=int)
    data = browsing_dao.domain_ranking(limit, within)
    count = len(data)
    headers = {"X-Data-Count": count}
    return Response(json.dumps(data),
                    mimetype='application/json',
                    headers=headers)

@v1.route('/rankings/src_ip', methods=['GET'])
def src_ip_ranking():
    limit = request.args.get('limit', default=10, type=int)
    within = request.args.get('within', default=30, type=int)
    data = browsing_dao.src_ip_ranking(limit, within)
    count = len(data)
    headers = {"X-Data-Count": count}
    return Response(json.dumps(data),
                    mimetype='application/json',
                    headers=headers)

@v1.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    if keyword:
        data = list(browsing_dao.search(keyword, cols))
        count = len(data)
    else:
        data = list(browsing_dao.get_with_browsing_time(cols))
        all_data = browsing_dao.count_all()
        count = all_data
    headers = {"X-Data-Count": count}
    return Response(json.dumps(data),
                    mimetype='application/json',
                    headers=headers)

@v1.route('/word', methods=['GET'])
def word_cloud():
    data = word_dao.get(30)
    count = len(data)
    headers = {"X-Data-Count": count}
    return Response(json.dumps(data),
                    mimetype='application/json',
                    headers=headers)


@v1.route('/histogram/http', methods=['GET'])
def http_histogram():
    per = request.args.get('per', default=10, type=int)
    num = request.args.get('num', default=28, type=int)
    data = browsing_dao.http_histogram(per, num)
    count = len(data)
    headers = {"X-Data-Count": count}
    return Response(json.dumps(data),
                    mimetype='application/json',
                    headers=headers)
