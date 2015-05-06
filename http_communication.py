import sqlite3
import hashlib
import re


class HTTP:
    def __init__(self, src_ip, dst_ip, src_port, dst_port, timestamp):
        self.timestamp = timestamp
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self._uri = None
        self._host = None
        self._content_type = None
        self._title = None

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, value):
        self._uri = value

    @property
    def url(self):
        """

        >>> http = HTTP('1.1.1.1', '2.2.2.2', 80, 1234, '2014/1/1 00:00:00')
        >>> http.url
        >>> http.host = 'google.com'
        >>> http.uri = '/search'
        >>> http.url
        'http://google.com/search'
        """
        if self._uri and self._host:
            return "http://" + self._host + self._uri

    @property
    def context_type(self):
        return self._content_type

    @context_type.setter
    def content_type(self, value):
        self._content_type = value

    def five_tuple_key(self):
        """
            Generate Hash key
            hash is generated from src ip, dst ip, src port and dst port

            >>> x = HTTP('2.2.2.2', '1.1.1.1', 1234, 80, '2014/1/1 00:00:00')
            >>> y = HTTP('1.1.1.1', '2.2.2.2', 80, 1234, '2014/1/1 00:00:00')
            >>> x.five_tuple_key() == y.five_tuple_key()
            True
        """
        keys = [self.src_ip,
                self.dst_ip,
                str(self.src_port),
                str(self.dst_port)]
        key = "".join(sorted(keys))
        hashed = hashlib.md5(key.encode('utf-8'))
        return hashed.hexdigest()

    def is_valid(self):
        """
            Check url and uri are stored.

            >>> http = HTTP('1.1.1.1', '2.2.2.2', 80, 1234, '2014/1/1 00:00:00')
            >>> http.is_valid()
            False
            >>> http.host = 'google.com'
            >>> http.uri = '/'
            >>> http.is_valid()
            True
        """
        return self._uri is not None and self._host is not None


def is_request_and_response_pair(request, response):
    """
        Check if request and response pair
        dst and src ip and dst and src port would be opposite

        >>> x = HTTP('2.2.2.2', '1.1.1.1', 1234, 80, '2014/1/1 00:00:00')
        >>> y = HTTP('1.1.1.1', '2.2.2.2', 80, 1234, '2014/1/1 00:00:00')
        >>> is_request_and_response_pair(x, y)
        True
    """
    if not isinstance(request, HTTP) and isinstance(response, HTTP):
        return False

    if (request.src_ip == response.dst_ip and
        request.dst_ip == response.src_ip and
        request.src_port == response.dst_port and
        request.dst_port == response.src_port):
        return True
