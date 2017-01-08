# Copyright (c) 2017 Akuli

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Set up BananaGUI."""

import os
import re
import sys

try:
    import bananagui
except ImportError:
    # Python 3.2 or 3.3, enum is not installed yet.
    bananagui = None

from setuptools import find_packages, setup


def get_extra_kwargs():
    kwargs = {}
    if bananagui is None:
        with open(os.path.join('bananagui', '__init__.py'), 'r') as f:
            for line in f:
                line = line.rstrip('\n')
                match = re.search(r'''^(__.*__) = ['"](.*)['"]$''', line)
                if match is None:
                    continue
                name, value = match.groups()
                if name == '__version__':
                    kwargs['version'] = value
                if name == '__author__':
                    kwargs['author'] = value
                if name == '__license__':
                    kwargs['license'] = value
    else:
        kwargs['version'] = bananagui.__version__
        kwargs['author'] = bananagui.__author__
        kwargs['license'] = bananagui.__license__
    return kwargs


installreq = []
if sys.version_info[:2] < (3, 4):
    installreq.append('enum34')

setup(name='bananagui',
      description="wrapper for popular GUI toolkits",
      url='https://github.com/Akuli/BananaGUI/',
      packages=find_packages(include=['bananagui', 'bananagui.*']),
      install_requires=installreq,
      entry_points={
        'console_scripts': ['iniloader=bananagui.iniloader:main'],
      },
      **get_extra_kwargs())
