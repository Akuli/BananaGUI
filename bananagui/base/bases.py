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

"""Base classes for various widgets."""

import bananagui
from bananagui import check, types


class WidgetBase(types.ObjectBase):
    """A widget baseclass.

    Properties:
        real_widget     R
            The real GUI toolkit widget that's being wrapped.
    """

    real_widget = types.Property('real_widget')


class ParentBase:
    """A widget that child widgets can use as their parent."""

    _bananagui_bases = ('WidgetBase',)


class ChildBase:
    """A widget that can be added to a container.

    Children take a parent argument on initialization. The parent
    property can be used to retrieve it, but the parent cannot be
    changed afterwards.

    Properties:
        expand          RW
            Two-tuple of horizontal and vertical expanding.
            For example, (True, True) will make the widget expand in
            both directions. (False, False) by default.
        grayed_out      RW
            True if the widget is grayed out, False otherwise.
        parent          R
            The parent of this widget.
        tooltip         RW
            The widget's tooltip text, or None if the widget doesn't
            have a tooltip. None by default.
    """

    _bananagui_bases = ('WidgetBase',)
    parent = bananagui.Property('parent')
    expand = bananagui.Property('expand', checker=check.boolpair,
                                default=(False, False))
    grayed_out = bananagui.Property('grayed_out', required_type=bool,
                                    default=False)
    tooltip = bananagui.Property('tooltip', required_type=str,
                                 allow_none=True, default=None)

    def __init__(self, parent):
        super().__init__()
        self.raw_set('parent', parent)


class BinBase:
    """A widget that contains one child widget or no children at all.

    Properties:
        child           RW
            The child in the widget, None by default. Setting this to
            None removes the child.
    """

    _bananagui_bases = ('ParentBase',)
    child = bananagui.Property('child', allow_none=True, default=None)

    def _bananagui_set_child(self, child):
        # This isinstance check actually works because the loaded
        # ChildBase in bananagui.gui inherits from the ChildBase in this
        # module.
        assert isinstance(child, ChildBase), \
            "children must be BananaaGUI child widgets"
        assert child is None or child['parent'] is self, \
            "the child has the wrong parent"
        super()._bananagui_set_child(child)
