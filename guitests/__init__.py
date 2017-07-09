"""BananaGUI tests.

This file sets up a BananaGUI wrapper. If you use the -m option to run
the tests, this file will always be ran also.
"""

import faulthandler
import sys

# Not all GUI toolkits raise pythonic exceptions when something's wrong.
faulthandler.enable()   # noqa

import bananagui


# We need to ignore everything except the last argument because there
# are coverage's arguments in sys.argv when this is running under
# coverage.
if len(sys.argv) < 2:
    print("Usage: yourpython -m guitests WRAPPERMODULE",
          "       yourpython -m guitests.SUBMODULE WRAPPERMODULE",
          sep='\n', file=sys.stderr)
    sys.exit(1)

bananagui.load(sys.argv[-1])
