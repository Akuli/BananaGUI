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
import os
import types
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
        if (isinstance(value, types.MethodType)
                and value.__self__ is self.__prop):
            # It's a bound method, create a partial. This is done to
            # methods only instead of all callables because there's also
            # callable instance attributes like getdefault.
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
                 checker=None, add_changed=True, settable=True,
                 **check_kwargs):
        """Initialize the property.

        If checker is None, bananagui.utils.check will be called with
        check_kwargs instead. See the set and get docstrings for
        explanations about other arguments.

        Properties can have a default value that does not pass the
        bananagui.utils.check.
        """
        assert default is None or getdefault is None, \
            "both default and getdefault were specified"

        self.name = name
        if getdefault is None:
            self.getdefault = lambda: default
        else:
            self.getdefault = getdefault
        self._checker = checker
        self._check_kwargs = check_kwargs
        self.doc = doc
        self.settable = settable

        self._values = weakref.WeakKeyDictionary()
        if add_changed:
            self.changed = Signal(
                name + '.changed',
                doc="This signal is emitted when %s changes." % name)

    def __repr__(self):
        """Clearly tell the user that this is not a Python @property."""
        return '<BananaGUI %s %r>' % (type(self).__name__, self.name)

    def raw_set(self, widget, value):
        """Set the value of the BananaGUI property.

        This is called raw_set because it sets the value directly to the
        dictionary of set values. This also checks the value and emits
        the changed signal.
        """
        if self._checker is not None:
            self._checker(value)
        if self._check_kwargs:
            utils.check(value, **self._check_kwargs)
        old_value = self.get(widget)
        self._values[widget] = value
        if hasattr(self, 'changed'):
            self.changed.emit(widget, old_value=old_value, new_value=value)

    def set(self, widget, value):
        """Set the value of a BananaGUI property.

        This is a higher-level alternative to raw_set, and it works like
        this:
          - Make sure the property is settable.
          - Abort the setting process if the current value is equal to
            the new value.
          - Get the setter. It is the widget's attribute
            _bananagui_set_<name of the property>.
          - Call the setter with the converted value as the only argument.
          - Call raw_set.
        """
        if not self.settable:
            raise ValueError("the value of the BananaGUI %r %r cannot be set"
                             % (type(self).__name__, self.name))
        try:
            setter = getattr(widget, '_bananagui_set_' + self.name)
        except AttributeError as e:
            raise NotImplementedError("no setter was defined for %r"
                                      % self.name) from e
        if self.get(widget) == value:
            return
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

    def __get__(self, instance, cls=None):
        """Make the BananaGUI property behave like functions in classes."""
        if instance is None:
            # This is invoked from a class.
            return self
        # This is invoked from an instance.
        return _PropertyWrapper(self, instance)

    @classmethod
    def filepath(cls, name, **kwargs):
        """Create a property suitable for storing a path to a file."""
        def check_filepath(filepath):
            if filepath is not None:
                assert os.path.isfile(filepath), \
                    "%r is not a path to a file" % (filepath,)

        # We can't use collections.ChainMap because it's new in
        # Python 3.3.
        real_kwargs = {'type': str, 'allow_none': True, 'default': None,
                       'checker': check_filepath}
        real_kwargs.update(kwargs)
        return cls(name, **real_kwargs)

    @classmethod
    def imagepath(cls, name, **kwargs):
        """Like filepath, but append a notice about filetypes to doc."""
        kwargs['doc'] = kwargs['doc'].rstrip() + """

        Supported filetypes depend on the GUI toolkit. I recommend using
        `.png` and `.jpg` files because most GUI toolkits support them.
        """
        return cls.filepath(name, **kwargs)


class Event(structures.NamespaceBase):
    """An attribute container."""


class Signal(Property):
    """A property that contains callbacks and can be emitted."""

    def __init__(self, name, *, doc):
        """Initialize the signal."""
        super().__init__(name, getdefault=list, type=list,
                         add_changed=False, doc=doc)
        self._blocked = weakref.WeakSet()

    def set(self, widget, value):
        """Set the content of the current value to a new value."""
        self.raw_set(widget, value)

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

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            self[name] = value

    def __get_prop(self, propertyname):
        """Return a BananaGUI property."""
        result = self
        try:
            for attribute in propertyname.split('.'):
                result = getattr(result, attribute)
        except AttributeError as e:
            raise ValueError("no such BananaGUI property: %r"
                             % propertyname) from e
        if not isinstance(result, _PropertyWrapper):
            raise TypeError("%r is not a BananaGUI property" % propertyname)
        return result

    def __setitem__(self, name: str, value):
        self.__get_prop(name).set(value)

    def __getitem__(self, name: str):
        return self.__get_prop(name).get()

    # The set and get docstrings don't talk about things like set and
    # get because the same docstrings are reused here.
    __setitem__.__doc__ = Property.set.__doc__
    __getitem__.__doc__ = Property.get.__doc__


def _bool2string(value):
    return 'yes' if value else 'no'


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
            Settable:             yes
    >>> @bananadoc
    ... class Thingy(Thing):
    ...     """Thingy doc.
    ...
    ...     This thingy doc is multiple lines long.
    ...     """
    ...     b = Property(
    ...         'b', default="hello", settable=False,
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
            Settable:             yes
    <BLANKLINE>
          b
            Here's the b doc.
    <BLANKLINE>
            It's multiple lines long also.
    <BLANKLINE>
            Default value:        'hello'
            Has a changed signal: yes
            Settable:             no
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
        Has a changed signal: %(has-changed)s
        Settable:             %(settable)s\n\n''' % {
            'propname': prop.name,
            'propdoc': prop.doc.strip(),
            'default': prop.getdefault(),
            'has-changed': _bool2string(hasattr(prop, 'changed')),
            'settable': _bool2string(prop.settable),
        }

    if something_found:
        # There are BananaGUI properties so we can change the docstring.
        bananaclass.__doc__ = result.rstrip()

    return bananaclass


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
