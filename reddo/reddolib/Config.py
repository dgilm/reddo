import xml.sax
import sys


class ConfigHandler(xml.sax.handler.ContentHandler):

    def __init__(self):
        self.__config = {}
        xml.sax.handler.ContentHandler.__init__(self)

    def startElement(self, name, attrs):

        if name == "servers":
            self.__config["servers"] = {
                'filename': attrs.getValue("filename")
            }

        if name == "default":
            self.__config["default"] = {
                'name': attrs.getValue("name"),
                'langpair': attrs.getValue("langpair")
            }

    def get_config(self):

        return self.__config


class Config:

    def __init__(self, filename):
        self.__filename = filename
        self.__config = self.__read_config()

    def __read_config(self):

        # init parser and set XML Handler
        parser = xml.sax.make_parser()
        handler = ConfigHandler()
        parser.setContentHandler(handler)

        # let's go to parse!
        try:
            parser.parse(self.__filename)
        except IOError, e:
            print >>sys.stderr, "Error reading config file!\n", e
            sys.exit()

        return handler.get_config()

    def __getitem__(self, item):
        return self.__config[item]

    def __repr__(self):
        return self.__config.__repr__()


if __name__ == "__main__":

    config = Config("etc/config.xml")
    print config


# vim:ts=4 sts=4 tw=79 expandtab:
