from .basewidgets import Child


class Checkbox(Child):

    def set_text(self, text):
        pass

    def set_checked(self, checked):
        pass


class Dummy(Child):
    pass


class Separator(Child):

    def __init__(self, bananawidget, orientation):
        self.orientation = orientation
        super().__init__(bananawidget)
