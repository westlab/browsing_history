import time
from datetime import datetime

from http_communication import HTTPCommunication, is_request_and_response_pair
from browsing_dao import BrowsingDao


class BrowsingReconstruct:
    def __init__(self, db, timeout=60*30):
        self._http_comms = {}
        self._timeout = timeout # Seconds
        self._counter = 0
        self._browsing_dao = BrowsingDao(db)

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
            if not http_comm.five_tuple_key in self._http_comms:
                return

            if self._http_comms[key].stream_id == http_comm.stream_id:
                self._http_comms[key].host = http_result.result

        if http_result.pattern == 'Content-Type:':
            if not http_comm.five_tuple_key in self._http_comms:
                return

            if is_request_and_response_pair(self._http_comms[key], http_comm):
                self._http_comms[key].content_type = http_result.result

        if http_result.pattern == '<title':
            if not http_comm.five_tuple_key in self._http_comms:
                return

            if is_request_and_response_pair(self._http_comms[key], http_comm):
                self._http_comms[key].title = http_result.result

                # Check http comm is valid or not
                if self._is_http_comm_valid(key):
                    self._save_browsing(key)
                del self._http_comms[key]

        self._counter += 1
        if self._counter > 1000:
            self._gc()
            self._counter = 0

    def _is_http_comm_valid(self, key):
        http_comm = self._http_comms[key]
        repr(http_comm)
        if not http_comm.is_valid():
            return False

        if not http_comm.content_type == 'text/html':
            return False

        if http_comm.title is None:
            return False

        return True

    def _save_browsing(self, key):
        # self._browsing_dao.save(self._http_comms[key])
        print(self._http_comms[key].url, self._http_comms[key].title)

    def _gc(self):
        current_time = datetime.now()
        gc_keys = []

        for key, http_comm in self._http_comms.items():
            d = current_time - http_comm.created_at
            if d.total_seconds() > self._timeout:
                gc_keys.append(key)

        for key in gc_keys:
            del self._http_comms[key]
