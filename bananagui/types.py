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

from bananagui import utils, structures


class _PropertyWrapper:
    """Like types.MethodType but for BananaGUI properties."""

    def __init__(self, prop, instance):
        self.__prop = prop
        self.__instance = instance

    def __repr__(self):
        return ('<BananaGUI property wrapper of %r and %r>'
                % (self.__prop, self.__instance))

    def __dir__(self):
        return dir(self.__prop)

    def __getattr__(self, attribute):
        # The values are setattr()ed to self after getting them to avoid
        # calling this method repeatedly many times. If self has the
        # requested attribute, __getattr__ is not called. This way
        # self.__dict__ acts as a cache.
        #
        # https://docs.python.org/3/reference/datamodel.html#object.__getattr__
        value = getattr(self.__prop, attribute)
        if callable(value):
            # It's a method, create a partial.
            result = functools.partial(value, self.__instance)
        elif isinstance(value, Property):
            # It's a nested BananaGUI property, create another wrapper.
            result = _PropertyWrapper(value, self.__instance)
        else:
            # It's something else.
            result = value
        setattr(self, attribute, result)
        return result


class Property:
    """A basic property.

    The properties are not like Python properties with descriptor magic.
    They are more like properties in large GUI toolkits like Qt and
    GTK+.
    """

    def __init__(self, name, *, doc, default=None, getdefault=None,
                 checker=None, add_changed=True, **check_kwargs):
        """Initialize the property.

        If checker is None, bananagui.utils.check will be called with
        check_kwargs instead. See the set and get docstrings for
        explanations about other arguments.

        Properties can have a default value that does not pass the
        bananagui.utils.check.
        """
        assert default is None or getdefault is None, \
            "both default and getdefault were specified"
        assert checker is None or not check_kwargs, \
            "both checker and additional keyword arguments were specified"

        self.name = name
        if getdefault is None:
            self.getdefault = lambda: default
        else:
            self.getdefault = getdefault
        if checker is None:
            self.checker = functools.partial(utils.check, **check_kwargs)
        else:
            self.checker = checker
        self.doc = doc

        self._values = weakref.WeakKeyDictionary()
        if add_changed:
            self.changed = Signal(
                name + '.changed',
                doc="This signal is emitted when %s changes." % name)

    def __repr__(self):
        """Clearly tell the user that this is not a Python @property."""
        return '<BananaGUI %s %r>' % (type(self).__name__.lower(), self.name)

    def raw_set(self, widget, value):
        """Set the value of the BananaGUI property.

        This is called raw_set because it sets the value directly to the
        dictionary of set values. This also checks the value and emits
        the changed signal.
        """
        self.checker(value)
        old_value = self.get(widget)
        self._values[widget] = value
        if hasattr(self, 'changed'):
            self.changed.emit(widget, old_value=old_value, new_value=value)

    def set(self, widget, value):
        """Set the value of a BananaGUI property.

        This is a higher-level alternative to raw_set, and it works like
        this:
          - Make sure the widget's type has a setter. The setter is
            widget._bananagui_set_NAME.
          - Run the checker. It should raise an exception if the value
            is not correct.
          - Call the setter with the widget and the converted value
            as arguments.
          - Call self.raw_set.
        """
        try:
            setter = getattr(widget, '_bananagui_set_' + self.name)
        except AttributeError as e:
            msg = "the value of the BananaGUI property %r cannot be set"
            raise ValueError(msg % self.name) from e
        setter(value)
        self.raw_set(widget, value)

    def get(self, widget):
        """Get the value of a BananaGUI property.

        Try to get the value from the dictionary of values that are set.
        If it fails, use getdefault or default. getdefault will be
        called without arguments.
        """
        # We can't use self._values.setdefault(widget, self._getdefault())
        # because then self._getdefault() would be also called when it's
        # not needed.
        try:
            value = self._values[widget]
        except KeyError:
            value = self._values[widget] = self.getdefault()
        return value

    def __get__(self, instance, cls):
        """Make the BananaGUI property behave like functions in classes."""
        if instance is None:
            # This is invoked from a class.
            return self
        # This is invoked from an instance.
        return _PropertyWrapper(self, instance)


class Event(structures.NamespaceBase):
    pass


class Signal(Property):
    """A property that contains callbacks and can be emitted."""

    def __init__(self, name, *, doc):
        """Initialize a signal."""
        super().__init__(name, getdefault=list, type=list,
                         add_changed=False, doc=doc)
        self._blocked = weakref.WeakSet()

    def connect(self, widget, function, *args, **kwargs):
        """Add bananagui.Callback(function, *args, **kwargs) to self."""
        callback = structures.Callback(function, *args, **kwargs)
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


class BananaObject:
    """A base class for using BananaGUI properties and signals."""

    def __get_prop(self, propertyname):
        """Return a BananaGUI property."""
        assert isinstance(propertyname, str)

        result = self
        try:
            for attribute in propertyname.split('.'):
                result = getattr(result, attribute)
        except AttributeError as e:
            msg = "no such BananaGUI property: %r" % propertyname
            raise ValueError(msg) from e

        if not isinstance(result, _PropertyWrapper):
            raise TypeError("%r is not a BananaGUI property" % propertyname)
        return result

    @utils.copy_doc(Property.set)
    def __setitem__(self, name, value):
        self.__get_prop(name).set(value)

    @utils.copy_doc(Property.get)
    def __getitem__(self, name):
        return self.__get_prop(name).get()


def bananadoc(bananaclass):
    '''Add documentation to a BananaObject subclass from its properties.

    Use this as a decorator, like this:

    >>> @bananadoc
    ... class Thing(BananaObject):
    ...     """Thing doc."""
    ...     a = Property('a', doc="Here's the a doc.")
    ...
    >>> print(Thing.__doc__)
    Thing doc.
    <BLANKLINE>
        ----------------------------------------------------------------------
    <BLANKLINE>
        BananaGUI properties:
          a
            Here's the a doc.
    <BLANKLINE>
            Default value:        None
            Has a changed signal: yes
    >>> @bananadoc
    ... class Thingy(Thing):
    ...     """Thingy doc.
    ...
    ...     This thingy doc is multiple lines long.
    ...     """
    ...     b = Property(
    ...         'b', default="hello",
    ...         doc="""Here's the b doc.
    ...
    ...         It's multiple lines long also.
    ...         """)
    ...
    >>> print(Thingy.__doc__)
    Thingy doc.
    <BLANKLINE>
        This thingy doc is multiple lines long.
    <BLANKLINE>
        ----------------------------------------------------------------------
    <BLANKLINE>
        BananaGUI properties:
          a
            Here's the a doc.
    <BLANKLINE>
            Default value:        None
            Has a changed signal: yes
    <BLANKLINE>
          b
            Here's the b doc.
    <BLANKLINE>
            It's multiple lines long also.
    <BLANKLINE>
            Default value:        'hello'
            Has a changed signal: yes
    >>>
    '''
    if bananaclass.__doc__ is None:
        # Python is being ran with the optimizations turned on or the
        # class is not documented for some reason.
        return bananaclass

    result = bananaclass.__doc__.rstrip() + '''

    %(dashes)s

    BananaGUI properties:\n''' % {'dashes': '-'*70}

    something_found = False
    for name in dir(bananaclass):
        if name.startswith('_'):
            # Something non-public.
            continue

        prop = getattr(bananaclass, name)
        if not isinstance(prop, Property):
            # Can't add it to documentation.
            continue

        something_found = True

        result += '''\
      %(propname)s
        %(propdoc)s

        Default value:        %(default)r
        Has a changed signal: %(has-changed)s\n\n''' % {
            'propname': prop.name,
            'propdoc': prop.doc.strip(),
            'default': prop.getdefault(),
            'has-changed': 'yes' if hasattr(prop, 'changed') else 'no',
        }

    if something_found:
        # There are BananaGUI properties so we can change the docstring.
        bananaclass.__doc__ = result.rstrip()

    return bananaclass


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
