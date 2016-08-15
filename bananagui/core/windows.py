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

"""Window widgets for BananaGUI.

This module has nothing to do with Windows the operating system.
"""

from bananagui.core import Property, bases


class WindowBase(bases.SingleContainerBase):
    """A window baseclass.

    Properties:
        title           RW
            The title of the window. 'Window' by default.
        resizable       RW
            True if the window can be resized, False otherwise.
        showing         RW
            True if the window is showing, False by default.
            Closing the window sets this to False. Connect to the
            changed signal if you want to run something when the window
            is closed.
        width           RWC
            The width of the window, 200 by default.
        height          RWC
            The height of the window, 200 by default.
        size            RWC
            Two-tuple of width and height
    """

    title = Property(converter=str, default="Window")
    resizable = Property(converter=bool, default=True)
    showing = Property(converter=bool, default=False)
    width = Property.nonnegative(converter=int, default=200)
    height = Property.nonnegative(converter=int, default=200)
    size = Property.tuplealias('width', 'height')


class ParentWindow(WindowBase):
    """A window that can have child windows.

    You can create multiple main windows.
    """


class ChildWindow(WindowBase):
    """A window that has a parent window.

    On initialization, the window takes a parentwindow argument. This
    window may be centered over the parent window, it may be modal or
    whatever the real GUI toolkit supports.

    Properties:
        parentwindow    R
            A MainWindow instance.
    """

    parentwindow = Property(required_type=ParentWindow)

    def __init__(self, parentwindow):
        self.parentwindow.raw_set(self, parentwindow)
