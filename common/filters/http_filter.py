from urllib.parse import urlparse

class HttpFilter:
    def __init__(self):
        self._file_ex = ['jpeg', 'gif', 'png', 'ico', 'jpg']
        self._status = ['301', '202', '307', '401', '404', '500', '303', '302']
        self._title = ['bit.ly', 'PR', 'Advertisement', 'Twitter Tweet Button',
                'はてなブックマークボタン', 'Object moved']

    def url(self, url):
        """
        Return False if contain non relevent file extension

        >>> hf = HttpFilters()
        >>> hf.url("http://google.com")
        True
        >>> hf.url("http://google.com?q=jpg")
        True
        >>> hf.url("http://google.com/west.png")
        False
        """
        o = urlparse(url)
        if o:
            if o.path.split('.')[-1] not in self._file_ex:
                return True
            else:
                return False
        else:
            return True

    def title(self, title):
        """
        Return False if contains non relevent information

        >>> hf.title('hoge')
        True
        >>> hf.title('404 Not Found')
        False
        >>> hf.title('Not Found 404')
        False
        """
        for banned_status in self._status + self._title:
            if banned_status in title:
                return False
        else:
            return True
