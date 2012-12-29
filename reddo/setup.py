#!/usr/bin/env python

from distutils.core import setup

import glob, os

doc = [ ('share/doc/reddo', ['doc/INSTALL', 'doc/COPYING',
                             'doc/AUTHORS', 'doc/TODO', 'doc/ChangeLog'] )]

man  = [ ('share/man/man1', ['doc/reddo.1.gz']) ]

lib  = [ ('share/reddo/reddolib',
            glob.glob(os.path.join('reddolib', '*.py'))) ]

etc = [ ('/etc/reddo',
            glob.glob(os.path.join('etc', '*.xml')) ),
        ('/etc/reddo/servers',
            glob.glob(os.path.join('etc', 'servers', '*.xml'))) ]

data = etc + doc + man + lib


from reddolib.__init__ import VERSION

setup (
    name            = "reddo",
    version         = VERSION,
    description     = "Reddo Internet Translator",
    author          = "Reddo Development Team",
    author_email    = "reddo-developers@lists.sourceforge.net",
    url             = "http://reddo.sf.net",
    license         = "GPL",
#    packages        = [ 'reddolib' ],
    scripts         = [ 'reddo' ],
    data_files      = data
)

