import os
import subprocess
import sys

try:
    import faulthandler
    faulthandler.enable()
except ImportError:
    # I think faulthandler is new in... maybe 3.4? I don't know.
    pass


here = os.path.dirname(os.path.abspath(__file__))

listing = os.listdir(here)
listing.sort()
for filename in listing:
    name, extension = os.path.splitext(filename)
    if extension == '.py' and not name.startswith('_'):
        print((" %s " % filename).center(70, '*'))
        subprocess.call([sys.executable, '-m', 'guitests.%s' % name])
