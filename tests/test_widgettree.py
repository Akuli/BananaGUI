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

import pytest

from bananagui import widgets, widgettree


asciitemplate = """\
{window}
`-- {bigbox}
    |-- {labelbox}
    |   |-- {label1}
    |   |-- {label2}
    |   `-- {label3}
    `-- {button}
"""
unicodetemplate = (asciitemplate
                   .replace('`-- ', '└── ')
                   .replace('|-- ', '├── ')
                   .replace('|   ', '│   '))


def test_dumping(dummywrapper, capsys):
    window = widgets.Window("Test window")
    bigbox = widgets.Box()
    window.add(bigbox)
    labelbox = widgets.Box()
    bigbox.append(labelbox)
    for i in (1, 2, 3):
        labelbox.append(widgets.Label("Label %d" % i))
    button = widgets.Button()
    bigbox.append(button)

    widgetlist = [
        ('window', window),
        ('bigbox', bigbox),
        ('labelbox', labelbox),
        ('label1', labelbox[0]),
        ('label2', labelbox[1]),
        ('label3', labelbox[2]),
        ('button', button),
    ]
    asciiformat = {
        name: widgettree._clean_repr(widget, ascii_only=True)
        for name, widget in widgetlist}
    unicodeformat = {
        name: widgettree._clean_repr(widget, ascii_only=False)
        for name, widget in widgetlist}
    asciiresult = asciitemplate.format(**asciiformat)
    unicoderesult = unicodetemplate.format(**unicodeformat)
    assert widgettree.dumps(window) == unicoderesult
    assert widgettree.dumps(window, ascii_only=True) == asciiresult
    assert capsys.readouterr() == ('', '')  # check if it leaks to stdout
    widgettree.dump(window)
    assert capsys.readouterr() == (unicoderesult, '')
