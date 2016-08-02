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

"""The core of BananaGUI."""

import contextlib


class Property:
    """A Property.

    The Properties are more like properties in GUI toolkits like PyQt
    and GTK+ than Python properties. Add these to class instances on
    __init__, and document them in the class docstring.

    When the value of the property is changed, everything in the
    callback list will be called with the new value as the only
    argument. Note that setting a value equal to the property's current
    value doesn't trigger this.
    """

    # The properties are called explicitly instead of using __set__ and
    # __get__ to avoid interference with other attributes in subclasses,
    # e.g. `label.text = 'hello'` overwrites the property instead of
    # changing its value with descriptor magic. `label.text('hello')`
    # would change the value.

    def __init__(self, default_value):
        """Initialize the Property."""
        self.setter = None
        self.getter = None
        self.value = default_value
        self.callbacks = []

    def set(self, value):
        """Set the Property's value and run the callback functions."""
        if self.setter is None:
            raise ValueError("cannot set the value")
        with self.run_callbacks():
            self.setter(value)
            self.value = value

    def get(self):
        """Return the current value."""
        if self.getter is None:
            return self.value
        return self.getter()

    @contextlib.contextmanager
    def run_callbacks(self):
        """Run the callbacks if the value changes.

        Get the value in the beginning, yield and get the value at the
        end. If the values are not equal, call the callbacks with the
        new value as the only argument.
        """
        old_value = self.get()
        yield
        new_value = self.get()
        if old_value != new_value:
            for callback in self.callbacks:
                callback(new_value)


class _ItemGetter:
    """When an instance is subscripted, call a function given on __init__.

    The function is given whatever is subscripted with the only
    argument, and its return value will be returned.
    """

    def __init__(self, function):
        """Assign function to self._function."""
        self._function = function

    def __getitem__(self, item):
        """Return self._function(item)."""
        return self._function(item)


class BaseObject:
    """An object that implements the properties."""

    def __init__(self):
        """Create the prop dict."""
        self.props = {}
        self.callbacks = _ItemGetter(self.__get_callback_list)

    def __get_callback_list(self, propname):
        return self.props[propname].callbacks

    def __setitem__(self, propname, value):
        """Set a property's value.

        Example:
            a_window['title'] = 'My title'
            a_window['size'] = (300, 200)  # parenthesis can be omitted
        """
        self.props[propname].set(value)

    def __getitem__(self, propname):
        """Return the current value of a property.

        Example:
            print('The window title is', a_window['title'])
            print('The window size is', a_window['size'])
        """
        return self.props[propname].get()
