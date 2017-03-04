from .basewidgets import Child, Widget


class Bin(Widget):

    def add(self, child):
        pass

    def remove(self, child):
        pass


class Box(Child):

    def __init__(self, bananawidget, orientation):
        self.orientation = orientation
        super().__init__(bananawidget)

    def append(self, child):
        pass

    def remove(self, child):
        pass


class Scroller(Bin, Child):
    pass


class Group(Bin, Child):

    def set_text(self, text):
        pass
