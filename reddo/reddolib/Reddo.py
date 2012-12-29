import sys
import urllib
import random
from optparse import OptionParser

import reddolib.Config
import reddolib.Servers
import reddolib.Query
import reddolib.Output


class Reddo:

    def __init__(self):
        self.__text = ""
        self.parse_options()
        self.read_config()

    def parse_options(self):

        from __init__ import VERSION

        usage = "%prog [options] [\"text to translate\"]"
        parser = OptionParser(usage=usage, version="reddo " + VERSION)
        parser.add_option("-v",
                          "--verbose",
                          dest="verbose",
                          action="store_true",
                          help="make lots of noise")
        parser.add_option("",
                          "--list-servers",
                          dest="list_servers",
                          action="store_true",
                          help="list supported servers")
        parser.add_option("",
                          "--list-langpairs",
                          dest="list_langpairs",
                          action="store_true",
                          help="list langpairs supported for each server")
        parser.add_option("-s",
                          "--server",
                          dest="server",
                          action="store",
                          help="use SERVER as translation server",
                          metavar="SERVER")
        parser.add_option("-l",
                          "--langpair",
                          dest="langpair",
                          action="store",
                          help="use LANGPAIR as translation langpair",
                          metavar="LANGPAIR")
        parser.add_option("-c",
                          "--config",
                          dest="config_file",
                          action="store",
                          help="read config from FILE",
                          metavar="FILE")
        (options, args) = parser.parse_args()

        if len(args) == 1:
            # Replace special characters in string using the "%xx" escape
            # Also replaces spaces by plus signs, as required for quoting
            # HTML form values
            self.__text = urllib.quote_plus(args[0])
        elif (options.list_servers is None and options.list_langpairs is None):
            parser.error("incorrect number of arguments")

        self.__options = options

    def read_config(self):

        # read config from config.xml and servers.xml
        config_file = '/etc/reddo/config.xml'
        if self.__options.config_file is not None:
            config_file = self.__options.config_file

        self.__config = reddolib.Config.Config(config_file)
        self.__servers = reddolib.Servers.Servers(
            self.__config["servers"]["filename"])

    def translate(self):

        # --list-servers
        if self.__options.list_servers:
            for s in self.__servers.get_name_servers():
                mark = ""
                if self.__servers[s]["random"] == "yes":
                    mark = " (R)"
                print "%s: %s%s" % (s, self.__servers[s]["description"], mark)
            print "random: Special random server (servers marked with (R))"
            sys.exit()

        # --list-langpairs
        if self.__options.list_langpairs:
            if self.__options.server is not None:
                for lang in self.__servers.get_server_langpairs(
                        self.__options.server):
                    print lang
            else:
                print "Please, use -s option to select a server " +\
                      "(--list-servers to check servers)"
            sys.exit()

        # choose a server
        random.seed()
        rserver = random.choice(self.__servers.get_random_servers())
        if self.__options.server is not None:
            if self.__options.server == "random":
                server = self.__servers[random.choice(rserver)]
            else:
                server = self.__servers[self.__options.server]
        else:
            if self.__config['default']['name'] == "random":
                server = self.__servers[rserver]
            else:
                server = self.__servers[self.__config['default']['name']]

        if self.__options.verbose is not None:
            print "Using '%s'.." % (server["description"])

        # select langpair
        langpair = self.__config['default']['langpair']
        if self.__options.langpair is not None:
            langpair = self.__options.langpair

        # create params for server
        try:
            params = server['langpair'][langpair]['params']
        except KeyError:
            print >>sys.stderr, \
                "Sorry, langpair '%s' is not supported for this server" \
                % (langpair)
            sys.exit()
        params.append((server['input']['name'], self.__text))

        # obtain html from server
        result = reddolib.Query.Query(server['url'], params)
        html = result.read()

        # parse html
        parser = reddolib.Output.OutputParser(server['output']['tag'],
                                              server['output']['pos'],
                                              server['output']['regexp'])
        parser.feed(html)
        parser.close()

        # print result :)
        return parser.get_translation()


# vim:ts=4 sts=4 tw=79 expandtab:
