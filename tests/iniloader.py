import contextlib
import io
import textwrap
import unittest

import bananagui
from bananagui import iniloader


class LoadTest(unittest.TestCase):

    def setUp(self):
        if bananagui._wrapper is None:
            bananagui.load('tests.dummywrapper')
        elif bananagui._wrapper != 'tests.dummywrapper':
            raise RuntimeError(
                "bananagui.load() was called with %r, it should have "
                "been called with 'tests.dummywrapper'"
                % bananagui._wrapper)

    @contextlib.contextmanager
    def assert_raises_str(self, exctype, string):
        """Like assertRaises(), but checks str(the_exception)."""
        with self.assertRaises(exctype) as got:
            yield got
        if string is not None:
            self.assertEqual(str(got.exception), string)

    def test_errors(self):
        with self.assert_raises_str(
                SyntaxError,
                "invalid syntax (<string>, line 1)"):
            iniloader.load("this is invalid syntax")

        msg = ("the top of the ini file can only contain imports\n"
               "file '<string>', line 1\n"
               "  \"print('hello')\"")
        with self.assert_raises_str(iniloader.ParsingError, msg):
            iniloader.load("print('hello')")    # only imports

        msg = ("invalid ini syntax\n"
               "file '<string>', line 5\n"
               "  'blah blah blah\\n'")
        with self.assert_raises_str(iniloader.ParsingError, msg):
            # The newlines in the beginning shift the line numbers. The
            # iniloader should fix them.
            iniloader.load("\n\n\n[test]\nblah blah blah\n")

        msg = ("the second word of 3-word headers must be 'in'\n"
               "file '<string>'\n  '[banana and gui]'")
        with self.assert_raises_str(iniloader.ParsingError, msg):
            iniloader.load("[banana and gui]\n")

        msg = "undefined variable 'lol'\nfile '<string>'\n  '[banana in lol]'"
        with self.assert_raises_str(iniloader.ParsingError, msg):
            iniloader.load("[banana in lol]\n")

        msg = ("headers can contain one or three words, not 4\n"
               "file '<string>'\n  '[bla bla bla bla]'")
        with self.assert_raises_str(iniloader.ParsingError, msg):
            iniloader.load("[bla bla bla bla]\n")

        msg = ("invalid variable name 'bla bla'\n"
               "file '<string>'\n  'bla bla = 123'")
        with self.assert_raises_str(iniloader.ParsingError, msg):
            iniloader.load("[test]\nbla bla = 123\n")

    def test_loading(self):
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
        # Test the seeking with different encodings.
        nonefile = io.StringIO(content)
        assert nonefile.encoding is None
        utf8bytesio = io.BytesIO(content.encode())
        utf8file = io.TextIOWrapper(utf8bytesio)
        latin1bytesio = io.BytesIO(content.encode('latin-1'))
        latin1file = io.TextIOWrapper(latin1bytesio, encoding='latin-1')

        widgetdict1 = iniloader.load(content)
        widgetdict2 = iniloader.load(nonefile)
        widgetdict3 = iniloader.load(utf8file)
        widgetdict4 = iniloader.load(latin1file)
        for d in (widgetdict1, widgetdict2, widgetdict3, widgetdict4):
            self.assertEqual(d.keys(), {'window', 'box', 'label'})
            self.assertIs(d['window'].child, d['box'])
            self.assertEqual(d['box'][:], [d['label']])
            self.assertEqual(d['label'].text, 'hello multiline world')


if __name__ == '__main__':
    unittest.main()
