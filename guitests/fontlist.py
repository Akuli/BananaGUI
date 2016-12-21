# Copyright (c) 2016 Akuli

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

import math
import shutil

from bananagui import font


def print_table(thinglist):
    """Print a list of strings as a nice table."""
    maxlen = max(map(len, thinglist))
    columns = shutil.get_terminal_size().columns // (maxlen + 2)
    if columns < 2:
        for thing in thinglist:
            print(thing)
    else:
        rows = math.ceil(len(thinglist) / columns)
        for y in range(rows):
            string = '  '.join(item.ljust(maxlen)
                               for item in thinglist[y::rows])
            print(string.rstrip())


def main():
    families = sorted(font.get_families())
    print_table(families)


if __name__ == '__main__':
    main()
