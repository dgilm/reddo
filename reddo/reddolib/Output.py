from HTMLParser import HTMLParser
import re

class OutputParser(HTMLParser):

    def __init__ (self, tag, pos, regexp):
    
        self.__tag = tag
        self.__pos = int(pos)
        self.__pattern = re.compile(regexp)

        self.__current_tag = ""
        self.__current_pos = 1
        
        self.__translation = ""

        HTMLParser.__init__(self)


    def handle_starttag(self, tag, attrs):
        
        self.__current_tag = tag


    def handle_data (self, text):

        if self.__current_tag == self.__tag:
            if self.__current_pos == self.__pos:
                result = self.__pattern.search(text)
                if result is not None:
                    self.__translation = unicode(result.groups()[0], 'latin-1')
            self.__current_pos += 1


    def handle_endtag(self, tag):

        self.__current_tag = ""


    def get_translation(self):

        return self.__translation


if __name__ == "__main__":
    
    parser = OutputParser("p", 2, "(.*)")
    parser.feed("<html><p>hola</p><p>nackle</p></html>")
    parser.close()

    print parser.get_translation()


# vim:ts=4 sts=4 tw=79 expandtab:

