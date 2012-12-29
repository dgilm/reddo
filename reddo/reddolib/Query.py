import urllib
import sys


class ReddoURLopener(urllib.URLopener):

    def __init__(self):
        ReddoURLopener.version = "python-urllib"
        urllib.URLopener.__init__(self)


class Query:

    def __init__(self, url, params):
        self.__url = self.generateUrl(url, params)
        self.__html = ""

    def read(self):

        urlopener = ReddoURLopener()
        try:
            f = urlopener.open(self.__url)
        except IOError, e:
            print >>sys.stderr, e
            return ""
        else:
            self.__html = f.read()
            return self.sanitizeHtml()

    def sanitizeHtml(self):

        import re

        # babelfish returns malformed tags
        htmlconvert = [
            (r'(\w+=\"\w+\")\">', r'\1>'),
            (r' \\>', r' />'),
            (r' /\w>', r' />'),
            (r'<.?script.*>', ''),
        ]

        for convert in htmlconvert:
            self.__html = re.sub(convert[0], convert[1], self.__html)

        return self.__html

    def generateUrl(self, url, params):

        complete_url = url + "?"
        for key, value in params:
            complete_url += '&' + key + '=' + value
        return complete_url


if __name__ == "__main__":

    query = "http://translate.google.com/translate_t"
    params = [('text', 'fool'), ('langpair', 'en|es')]
    q = Query(query, params)
    print q.read()


# vim:ts=4 sts=4 tw=79 expandtab:
