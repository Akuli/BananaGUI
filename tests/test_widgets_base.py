import pytest

import bananagui


def must_be_abstract():
    return pytest.raises(
        TypeError, match=(r"Can't instantiate abstract class \w+ "
                          r"with abstract methods .*"))


def test_abstract_classes():
    with pytest.raises(
        TypeError, message=("cannot create instances of Widget directly, "
                            "use a subclass instead")):
        bananagui.Widget()
    with must_be_abstract():
        bananagui.ChildWidget()


class StupidWidget(bananagui.Widget):
    pass


def test_stupid_widget_subclass():
    with pytest.raises(RuntimeError, message=("subclasses of Widget must set "
                                              "self.real_widget before "
                                              "calling Widget.__init__()")):
        StupidWidget()


class KindaWorkingWidget(bananagui.Widget):

    def __init__(self):
        self.real_widget = 'lol'


def test_get_class_name_and_basic_repr():
    kww = KindaWorkingWidget()
    assert bananagui.Window()._get_class_name() == 'bananagui.Window'
    assert kww._get_class_name() == '%s.KindaWorkingWidget' % __name__
    assert repr(kww) == '<%s.KindaWorkingWidget widget>' % __name__


def test_tooltips():
    window = bananagui.Window()
    widget = bananagui.Label()
    window.add(widget)
    assert widget.tooltip is None
    widget.tooltip = 'hello'
    widget.tooltip = None
