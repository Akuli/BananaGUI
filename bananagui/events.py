import collections


class Event:

    def __init__(self, *args, widget):
        self.args = args
        self.widget = widget


class PropertyChangedEvent:

    def __init__(self, *, propertyname, new_value, **kwargs):
        super().__init__(**kwargs)
        self.propertyname = propertyname
        self.new_value = new_value
