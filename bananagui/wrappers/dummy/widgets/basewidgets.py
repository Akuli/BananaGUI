class Widget:

    def __init__(self, bananawidget):
        self.real_widget = None
        self.bananawidget = bananawidget

    def focus(self):
        pass


class Child(Widget):

    def set_expand(self, expand):
        pass

    def set_tooltip(self, tooltip):
        pass

    def set_grayed_out(self, grayed_out):
        pass
