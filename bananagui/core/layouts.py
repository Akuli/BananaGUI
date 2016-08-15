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

"""Layout widgets for BananGUI."""

from bananagui.core import Property, bases


class BoxBase(bases.ParentBase):
    """A widget that contains other widgets in a row.

    Properties:
        children        RC
            A tuple of children in this widget.
            Modify this with the prepend, append an remove methods.
    """

    children = Property(converter=tuple, default=())

    def add_start(self, child, expand=False):
        """Start add widgets from the beginning.

        If other widgets have been add_started
        """
        if child['parent'] is not self:
            raise ValueError("cannot prepend a child with the wrong parent")
        children = (child,) + self['children']
        self.children.raw_set(self, children)

    def append(self, child, expand=False):
        """Add a widget to the end."""
        if child['parent'] is not self:
            raise ValueError("cannot append a child with the wrong parent")
        children = self['children'] + (child,)
        self.children.raw_set(self, children)

    def remove(self, child):
        """Remove a widget from self."""
        children = list(self['children'])
        children.remove(child)
        self.children.raw_set(self, tuple(children))

    def clear(self):
        """Remove all widgets from self."""
        self.children.raw_set(self, ())


class HBox(BoxBase):
    """A horizontal box."""


class VBox(BoxBase):
    """A vertical box."""
