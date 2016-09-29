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

"""BananaGUI events and signals."""

import contextlib
import functools
import weakref

from bananagui import check, utils


class _PropertyWrapper:
    """Like types.MethodType but for BananaGUI properties."""

    def __init__(self, prop, instance):
        self.__prop = prop
        self.__instance = instance

    def __dir__(self):
        return dir(self.__prop)

    def __getattr__(self, attribute):
        value = getattr(self.__prop, attribute)
        if callable(value):
            # It's a method, create a partial.
            return functools.partial(value, self.__instance)
        if isinstance(value, Property):
            # It's a nested BananaGUI property, create another wrapper.
            return _PropertyWrapper(value, self.__instance)
        # It's something else.
        return value

    def __repr__(self):
        return ('<BananaGUI property wrapper of %r and %r>'
                % (self.__prop, self.__instance))


class Property:
    """A basic property.

    The properties are not like Python properties with descriptor magic.
    They are more like properties in large GUI toolkits like Qt and
    GTK+.
    """

    def __init__(self, name, *, default=None, getdefault=None,
                 checker=None, add_changed=True, **check_kwargs):
        """Initialize the property.

        If checker is None, utils.check will be called with check_kwargs
        instead. See the set and get docstrings for explanations about
        other arguments.
        """
        assert default is None or getdefault is None, \
            "both default and getdefault were specified"
        assert checker is None or not check_kwargs, \
            "both checker and additional keyword arguments were specified"

        self._name = name
        self._default = default
        self._getdefault = getdefault
        if checker is None:
            self._checker = lambda value: check.check(value, **check_kwargs)
        else:
            self._checker = checker

        self._propertywrappers = weakref.WeakKeyDictionary()
        self._values = weakref.WeakKeyDictionary()
        if add_changed:
            self.changed = Signal(name + '.changed')

    def __repr__(self):
        return '<BananaGUI property %r>' % self._name

    def raw_set(self, widget, value):
        """Set the value of the BananaGUI property.

        This is called raw_set because it sets the value directly to the
        dictionary of set values. This also checks the value and emits
        the changed signal.
        """
        self._checker(value)
        old_value = self.get(widget)
        self._values[widget] = value
        if hasattr(self, 'changed'):
            self.changed.emit(widget, old_value=old_value, new_value=value)

    def set(self, widget, value):
        """Set the value of a BananaGUI property.

        This is a higher-level alternative to raw_set, and it works like
        this:
          - Make sure the widget's type has a setter. The setter is
            TYPE_OF_WIDGET._bananagui_set_NAME.
          - Run the checker. It should raise an exception if the value
            is not correct.
          - Call the setter with the widget and the converted value
            as arguments.
          - Call raw_set().
        """
        try:
            setter = getattr(widget, '_bananagui_set_' + self._name)
        except AttributeError as e:
            msg = "the value of the BananaGUI property %r cannot be set"
            raise ValueError(msg % self._name) from e
        setter(value)
        self.raw_set(widget, value)

    def get(self, widget):
        """Get the value of a BananaGUI property.

        Try to get the value from the dictionary of values that are set.
        If it fails, use getdefault or default. getdefault will be
        called without arguments.
        """
        try:
            # Get the value from the dictionary.
            value = self._values[widget]
        except KeyError:
            # Create a new value and set it into the dictionary.
            if self._getdefault is not None:
                value = self._getdefault()
            else:
                value = self._default
            self._values[widget] = value
        return value

    def __get__(self, instance, cls):
        """Make the BananaGUI property behave like functions in classes."""
        if instance is None:
            # This is invoked from a class.
            return self
        try:
            wrapper = self._propertywrappers[instance]
        except KeyError:
            wrapper = _PropertyWrapper(self, instance)
            self._propertywrappers[instance] = wrapper
        return wrapper


class Event(utils.NamespaceBase):
    pass


class Signal(Property):
    """A property that contains callbacks and can be emitted."""

    def __init__(self, name):
        """Initialize a signal."""
        super().__init__(name, getdefault=list, required_type=list,
                         add_changed=False)
        self._blocked = weakref.WeakSet()

    def connect(self, widget, *args):
        """Append bananagui.Callback(*args) to self."""
        callback = bananagui.Callback(*args)
        self.get(widget).append(callback)

    def emit(self, widget, **kwargs):
        """Call the callbacks with an event created from arguments."""
        if widget in self._blocked:
            return
        event = Event(widget=widget, **kwargs)
        for callback in self.get(widget):
            callback(event)

    @contextlib.contextmanager
    def blocked(self, widget):
        """Block the signal from emitting temporarily.

        Blocking is widget-specific. Use this as a context manager.
        """
        self._blocked.add(widget)
        try:
            yield
        finally:
            self._blocked.remove(widget)


class ObjectBase:
    """A base class for using BananaGUI properties and signals."""

    def __get_prop(self, propertyname):
        """Return a BananaGUI property."""
        assert isinstance(propertyname, str)

        result = self
        try:
            for attribute in propertyname.split('.'):
                result = getattr(result, attribute)
        except AttributeError as e:
            raise ValueError("no such property: %r" % propertyname) from e

        assert isinstance(result, _PropertyWrapper), \
            "%r is not a BananaGUI property" % propertyname
        return result

    @utils.copy_doc(Property.set)
    def __setitem__(self, name, value):
        self.__get_prop(name).set(value)

    @utils.copy_doc(Property.get)
    def __getitem__(self, name):
        return self.__get_prop(name).get()
