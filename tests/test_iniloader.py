# Copyright (c) 2016-2017 Akuli

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

import io
import textwrap

import pytest

from bananagui import iniloader


def test_errors(dummywrapper):
    with pytest.raises(SyntaxError):
        iniloader.load("this is invalid syntax")

    with pytest.raises(iniloader.ParsingError) as got:
        iniloader.load("print('hello')")
    assert str(got.value) == (
        "the top of the ini file can only contain imports\n"
        "file '<string>', line 1\n  \"print('hello')\"")

    # The newlines in the beginning shift the line numbers. The
    # iniloader should fix them.
    with pytest.raises(iniloader.ParsingError) as got:
        iniloader.load("\n\n\n[test]\nblah blah blah\n")
    assert str(got.value) == (
        "invalid ini syntax\n"
        "file '<string>', line 5\n  'blah blah blah\\n'")

    with pytest.raises(iniloader.ParsingError) as got:
        iniloader.load("[banana and gui]\n")
    assert str(got.value) == (
        "the second word of 3-word headers must be 'in'\n"
        "file '<string>'\n  '[banana and gui]'")

    with pytest.raises(iniloader.ParsingError) as got:
        iniloader.load("[banana in lol]\n")
    assert str(got.value) == (
        "undefined variable 'lol'\nfile '<string>'\n  '[banana in lol]'")

    with pytest.raises(iniloader.ParsingError) as got:
        iniloader.load("[bla bla bla bla]\n")
    assert str(got.value) == (
        "headers can contain one or three words, not 4\n"
        "file '<string>'\n  '[bla bla bla bla]'")

    headers = ["[123abc]", "[def]", "[abc in 123abc]"]
    varnames = ["123abc", "def", "123abc"]
    for header, varname in zip(headers, varnames):
        with pytest.raises(iniloader.ParsingError) as got:
            iniloader.load(header + '\n')
        assert str(got.value) == (
            "invalid variable name %r\n"
            "file '<string>'\n  %r" % (varname, header))

    with pytest.raises(iniloader.ParsingError) as got:
        iniloader.load("[test]\nbla bla = 123\n")
    assert str(got.value) == (
        "invalid variable name 'bla bla'\n"
        "file '<string>'\n  'bla bla = 123'")


def test_loading(dummywrapper):
    content = textwrap.dedent("""\
    import bananagui
    from bananagui import widgets   # comment

    # non-ascii latin-1/utf-8 compatible characters for testing the seek:
    #   å¨¿¢«æßð

    [  window \t ]  # comment
    class = widgets.Window
    title = "test window"

    [  box  in\twindow ]
    class = widgets.Box
    orient = getattr(bananagui, 'VERTICAL')  # test built-ins

    [label in box]
    class = widgets.Label
    text = (
      "hello "
      "multiline "
      "world")
    """)
    # Different encodings for testing the seek.
    nonefile = io.StringIO(content)
    if nonefile.encoding is not None:
        raise ValueError
    utf8bytesio = io.BytesIO(content.encode())
    utf8file = io.TextIOWrapper(utf8bytesio)
    latin1bytesio = io.BytesIO(content.encode('latin-1'))
    latin1file = io.TextIOWrapper(latin1bytesio, encoding='latin-1')

    for source in (content, nonefile, utf8file, latin1file):
        widgetdict = iniloader.load(source)
        assert widgetdict.keys() == {'window', 'box', 'label'}
        assert widgetdict['window'].child is widgetdict['box']
        assert widgetdict['box'][:] == [widgetdict['label']]
        assert widgetdict['label'].text == 'hello multiline world'
