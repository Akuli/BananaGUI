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
    orientation = getattr(bananagui, 'HORIZONTAL')  # test built-ins

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
