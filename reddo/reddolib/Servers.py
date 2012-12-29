import xml.sax
import sys


class ServersHandler(xml.sax.handler.ContentHandler):

    def __init__(self):

        self.__current_server = ''
        self.__current_langpair = ''
        self.__servers = {}
        xml.sax.handler.ContentHandler.__init__(self)

    def startElement(self, name, attrs):

        if name == "server":
            self.__current_server = attrs.getValue("name")
            self.__servers[self.__current_server] = {
                'url': attrs.getValue("url"),
                'description': attrs.getValue("description"),
                'random': attrs.getValue("random"),
                'input': {},
                'output': {},
                'langpair': {}
            }
        if name == "input":
            self.__servers[self.__current_server]["input"] = {
                'name': attrs.getValue("name")
            }
        if name == "output":
            self.__servers[self.__current_server]["output"] = {
                'tag': attrs.getValue("tag"),
                'pos': attrs.getValue("pos"),
                'regexp': attrs.getValue("regexp"),
            }
        if name == "langpair":
            self.__current_langpair = attrs.getValue("id")
            self.__servers[self.__current_server]["langpair"]\
                [self.__current_langpair] = \
            {
                    'description': attrs.getValue("description"),
                    'params': []
            }
        if name == "param":
            self.__servers[self.__current_server]["langpair"]\
                [self.__current_langpair]["params"].append(
                    (attrs.getValue("name"), attrs.getValue("value")))

    def get_servers(self):

        return self.__servers


class Servers:

    def __init__(self, filename):
        self.__filename = filename
        self.__servers = self.__read_servers()

    def __read_servers(self):

        # init parser and set XML Handler
        parser = xml.sax.make_parser()
        handler = ServersHandler()
        parser.setContentHandler(handler)

        # let's go to parse!
        try:
            parser.parse(self.__filename)
        except IOError, e:
            print >>sys.stderr, "Error reading servers file!\n", e
            sys.exit()

        return handler.get_servers()

    def __getitem__(self, servername):

        try:
            item = self.__servers[servername]
        except KeyError:
            print >>sys.stderr, "Sorry, server '%s' is not supported" \
                % (servername)
            sys.exit()
        return item

    def __repr__(self):
        return self.__servers.__repr__()

    def __len__(self):
        return self.__servers.__len__()

    def get_name_servers(self):
        return self.__servers.keys()

    def get_random_servers(self):

        s = []
        for key, value in self.__servers.iteritems():
            if value["random"] == "yes":
                s.append(key)
        return s

    def get_server_langpairs(self, servername):

        if servername == "random":
            return []

        langs = []
        server = self.__servers[servername]
        for key, value in server["langpair"].iteritems():
            langs.append("%s: %s" % (key, value["description"]))
        return langs


if __name__ == "__main__":

    servers = Servers("../etc/servers.xml")
    print servers


# vim:ts=4 sts=4 tw=79 expandtab:
