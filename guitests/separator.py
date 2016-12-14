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

from bananagui import mainloop, widgets


def main():
    window = widgets.Window("Separator test")

    bigbox = widgets.Box.vertical(window)
    window.child = bigbox

    toplabel = widgets.Label(bigbox, "Top")
    bigbox.append(toplabel)

    hsep = widgets.Separator.horizontal(bigbox)
    bigbox.append(hsep)
    print(hsep)

    bottombox = widgets.Box.horizontal(bigbox)
    bigbox.append(bottombox)

    bottomleftlabel = widgets.Label(bottombox, "Bottom left")
    bottombox.append(bottomleftlabel)

    vsep = widgets.Separator.vertical(bottombox)
    bottombox.append(vsep)
    print(vsep)

    bottomrightlabel = widgets.Label(bottombox, "Bottom right")
    bottombox.append(bottomrightlabel)

    window.on_close.append(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
