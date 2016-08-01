"""The core of this wrapper."""

import contextlib
import copy


# A constant to allow setting None as the value for properties.
_NOTHING = object()


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

    def __init__(self, *value):
        """Initialize the Property.

        If value contains only one item, it's treated as the value.
        Property(1) means that the value is 1, and Property(1, 2) means
        that the value is (1, 2).
        """
        if len(value) == 1:
            value, = value
        self._setter = None
        self._getter = None
        self._value = default_value
        self.callbacks = []

    def __call__(self, *value):
        """Set or get the Property's value.

        See the note for Property.__init__. If the value is not given,
        return the current value.
        """
        if not value:
            # Get the value.
            if self._getter is None:
                return self._value
            return self._getter()
        # Set the value.
        if len(value) == 1:
            value = value[0]
        if self._setter is None:
            raise ValueError("cannot set the value")
        with self._run_callbacks():
            self._setter(value)
            self._value = value
        return None

    @contextlib.contextmanager
    def _run_callbacks(self):
        """Run the callbacks if the value changes.

        Get the value in the beginning, yield and get the value at the
        end. If the values are not equal, call the callbacks with the
        new value as the only argument.
        """
        old_value = self()
        yield
        new_value = self()
        if old_value != new_value:
            for callback in self.callbacks:
                callback(new_value)
