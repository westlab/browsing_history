import hashlib
from datetime import datetime

class HTTPCommunication:
    def __init__(self, id, src_ip, dst_ip, src_port, dst_port, timestamp, stream_id):
        self._id = id
        self.timestamp = timestamp
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.stream_id = stream_id
        self._uri = None
        self._host = None
        self._content_type = None
        self._title = None
        self._created_at = datetime.now()

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
            Return URL

            >>> http = HTTPCommunication(1, '1.1.1.1', '2.2.2.2', 80, 1234, '2014/1/1 00:00:00', 1)
            >>> http.url
            >>> http.host = 'google.com'
            >>> http.uri = '/search'
            >>> http.url
            'http://google.com/search'
        """
        if self.uri and self.host:
            return "http://" + self._host + self._uri

    @property
    def content_type(self):
        return self._content_type

    @content_type.setter
    def content_type(self, value):
        self._content_type = value

    @property
    def created_at(self):
        return self._created_at

    @property
    def five_tuple_key(self):
        """
            Generate Hash key
            hash is generated from src ip, dst ip, src port and dst port

            >>> x = HTTPCommunication(1, '2.2.2.2', '1.1.1.1', 1234, 80, '2014/1/1 00:00:00', 1)
            >>> y = HTTPCommunication(1, '1.1.1.1', '2.2.2.2', 80, 1234, '2014/1/1 00:00:00', 1)
            >>> x.five_tuple_key == y.five_tuple_key
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

            >>> http = HTTPCommunication(1, '1.1.1.1', '2.2.2.2', 80, 1234, '2014/1/1 00:00:00', 1)
            >>> http.is_valid()
            False
            >>> http.host = 'google.com'
            >>> http.uri = '/'
            >>> http.is_valid()
            True
        """
        return self.uri is not None and self.host is not None

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.__dict__)


def is_request_and_response_pair(request, response):
    """
        Check if request and response pair
        dst and src ip and dst and src port would be opposite

        >>> x = HTTPCommunication(1, '2.2.2.2', '1.1.1.1', 1234, 80, '2014/1/1 00:00:00', 1)
        >>> y = HTTPCommunication(1, '1.1.1.1', '2.2.2.2', 80, 1234, '2014/1/1 00:00:00', 2)
        >>> is_request_and_response_pair(x, y)
        True
    """
    if not isinstance(request, HTTPCommunication) and isinstance(response, HTTPCommunication):
        return False

    if (request.src_ip == response.dst_ip and
        request.dst_ip == response.src_ip and
        request.src_port == response.dst_port and
        request.dst_port == response.src_port):

        return True
