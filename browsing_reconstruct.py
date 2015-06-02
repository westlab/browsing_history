from datetime import datetime

from dto.http_communication import HTTPCommunication, is_request_and_response_pair
from common.filters.http_filter import HttpFilter
from common.logging.logger_factory import LoggerFactory


class BrowsingReconstruct:
    def __init__(self, browsing_dao, timeout=10):
        self._logger = LoggerFactory.create_logger(self)
        self._http_comms = {}
        self._timeout = timeout  # Seconds
        self._counter = 0
        self._browsing_dao = browsing_dao
        self._filters = HttpFilter()

    def add_http_result(self, http_result):
        http_comm = HTTPCommunication(http_result.id, http_result.src_ip,
                                      http_result.dst_ip, http_result.src_port,
                                      http_result.dst_port, http_result.timestamp,
                                      http_result.stream_id)

        key = http_comm.five_tuple_key
        if http_result.pattern == 'GET':
            http_comm.uri = http_result.result
            self._http_comms[key] = http_comm

        if http_result.pattern == 'Host:':
            if key not in self._http_comms:
                return

            if self._http_comms[key].stream_id == http_comm.stream_id:
                self._http_comms[key].host = http_result.result

        if http_result.pattern == 'Content-Type:':
            if key not in self._http_comms:
                return

            if is_request_and_response_pair(self._http_comms[key], http_comm):
                self._http_comms[key].content_type = http_result.result

        if http_result.pattern == '<title':
            if key not in self._http_comms:
                return

            if is_request_and_response_pair(self._http_comms[key], http_comm):
                self._http_comms[key].title = http_result.result

                # Check http comm is valid or not
                if self._is_http_comm_valid(key):
                    if self._apply_filters(self._http_comms[key]):
                        self._save_browsing(key)
                del self._http_comms[key]

        self._counter += 1
        if self._counter > 100000:
            self._gc()
            self._counter = 0

    def _is_http_comm_valid(self, key):
        http_comm = self._http_comms[key]
        if not http_comm.is_valid():
            return False

        if not http_comm.content_type == 'text/html':
            return False

        if not http_comm.title:
            return False

        return True

    def _apply_filters(self, http_comm):
        if not self._filters.url(http_comm.url):
            return False

        if not self._filters.title(http_comm.title):
            return False

        return True

    def _save_browsing(self, key):
        self._browsing_dao.save(self._http_comms[key])

    def _gc(self):
        current_time = datetime.now()
        gc_keys = []

        for key, http_comm in self._http_comms.items():
            d = current_time - http_comm.created_at
            if d.total_seconds() > self._timeout:
                gc_keys.append(key)

        for key in gc_keys:
            del self._http_comms[key]

        self._logger.info("{0} record are deleted".format(len(gc_keys)))
