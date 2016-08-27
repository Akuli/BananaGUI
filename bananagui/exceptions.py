class Error(Exception):
    """A base class for other BananaGUI exceptions."""


class PropertyOrSignalError(Error):
    """A property or signal error.

    This is in a separate class because sometimes BananaGUI doesn't know
    if the error is related to a property or a signal.
    """


class NoSuchPropertyOrSignal(PropertyOrSignalError):
    """A property is not found."""

    # For some reason, things like __init__ = KeyError.__init__ don't
    # work.
    def __init__(self, property_or_signal_name):
        super().__init__(property_or_signal_name)

    def __str__(self):
        return "the BananaGUI property or signal %r was not found" % self.args


# Currently, there are no PropertyError and SignalError classes, but
# they can be added later without breaking backwards compatibility.

class NotSettable(PropertyOrSignalError):

    def __init__(self, propertyname):
        super().__init__(propertyname)

    def __str__(self):
        return "the BananaGUI property %r cannot be set" % self.args
