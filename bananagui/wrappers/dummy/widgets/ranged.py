from .basewidgets import Child


class Slider(Child):

    def __init__(self, bananawidget, orientation, valuerange):
        super().__init__(bananawidget)

    def set_value(self, value):
        pass


class Spinbox(Child):

    def __init__(self, bananawidget, valuerange):
        super().__init__(bananawidget)

    def set_value(self, value):
        pass
