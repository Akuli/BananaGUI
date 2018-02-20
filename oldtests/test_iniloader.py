import io
import textwrap

import pytest

from bananagui import iniloader


def test_errors(dummywrapper):
    with pytest.raises(SyntaxError):
        iniloader.loads("this is invalid syntax")

    with pytest.raises(iniloader.ParsingError) as got:
        iniloader.loads("print('hello')")
    assert str(got.value) == (
        "the top of the ini file can only contain imports\n"
        "file '<string>', line 1\n  \"print('hello')\"")

    # The newlines in the beginning shift the line numbers. The
    # iniloader should fix them.
    with pytest.raises(iniloader.ParsingError) as got:
        iniloader.loads("\n\n\n[test]\nblah blah blah\n")
    assert str(got.value) == (
        "invalid ini syntax\n"
        "file '<string>', line 5\n  'blah blah blah\\n'")

    with pytest.raises(iniloader.ParsingError) as got:
        iniloader.loads("[banana and gui]\n")
    assert str(got.value) == (
        "the second word of 3-word headers must be 'in'\n"
        "file '<string>'\n  '[banana and gui]'")

    with pytest.raises(iniloader.ParsingError) as got:
        iniloader.loads("[banana in lol]\n")
    assert str(got.value) == (
        "undefined variable 'lol'\nfile '<string>'\n  '[banana in lol]'")

    with pytest.raises(iniloader.ParsingError) as got:
        iniloader.loads("[bla bla bla bla]\n")
    assert str(got.value) == (
        "headers can contain one or three words, not 4\n"
        "file '<string>'\n  '[bla bla bla bla]'")

    headers = ["[123abc]", "[def]", "[abc in 123abc]"]
    varnames = ["123abc", "def", "123abc"]
    for header, varname in zip(headers, varnames):
        with pytest.raises(iniloader.ParsingError) as got:
            iniloader.loads(header + '\n')
        assert str(got.value) == (
            "invalid variable name %r\n"
            "file '<string>'\n  %r" % (varname, header))

    with pytest.raises(iniloader.ParsingError) as got:
        iniloader.loads("[test]\nbla bla = 123\n")
    assert str(got.value) == (
        "invalid variable name 'bla bla'\n"
        "file '<string>'\n  'bla bla = 123'")


def cannot_seek(*args):
    raise io.UnsupportedOperation


def test_loading(dummywrapper):
    content = textwrap.dedent("""\
    from bananagui import Orient, widgets   # comment

    # non-ascii latin-1/utf-8 compatible characters for testing the seek:
    #   å¨¿¢«æßð

    [  window \t ]  # comment
    class = widgets.Window
    title = "test window"

    [  box  in\twindow ]
    class = widgets.Box
    orient = getattr(Orient, 'VERTICAL')  # test built-ins

    [label in box]
    class = widgets.Label
    text = (
      "hello "
      "multiline "
      "world")
    """)
    sources = []

    nonefile = io.StringIO(content)
    if nonefile.encoding is not None:
        raise ValueError
    sources.append(nonefile)

    # Test the seek-avoiding workaround.
    nonseekablefile = io.StringIO(content)
    nonseekablefile.seek = cannot_seek
    sources.append(nonseekablefile)

    # Test seeking with different encodings.
    for encoding in ('latin-1', 'utf-8'):
        bytefile = io.BytesIO(content.encode(encoding))
        file = io.TextIOWrapper(bytefile, encoding=encoding)
        sources.append(file)

    for source in sources:
        widgetdict = iniloader.load(source)
        if not isinstance(source, str):
            source.close()
        assert widgetdict.keys() == {'window', 'box', 'label'}
        assert widgetdict['window'].child is widgetdict['box']
        assert widgetdict['box'][:] == [widgetdict['label']]
        assert widgetdict['label'].text == 'hello multiline world'
