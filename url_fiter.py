import re
from urllib.parse import urlparse


class URLFilter:
    _file_extensions = ['.js', '.png', '.css', '.jpg', '.jpeg', '.gif']

    def is_valid(self, url):
        parsed_url = urlparse(url)
        if not parsed_url:
            return False

        for pattern in self._compile_fe_pattern():
            m = pattern.match(parsed_url.path)
            if m:
                return False

        return True

    def _compile_fe_pattern(self):
        return [lambda x: re.compile(x + '$') for x in self._file_extensions]
