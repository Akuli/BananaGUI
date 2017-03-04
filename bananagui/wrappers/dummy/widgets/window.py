from .parents import Bin


class Window(Bin):

    def __init__(self, bananawidget, title):
        super().__init__(bananawidget)

    def add(self, child):
        pass

    def set_title(self, title):
        pass

    def set_resizable(self, resizable):
        pass

    def set_size(self, size):
        pass

    def set_minimum_size(self, size):
        pass

    def set_hidden(self, hidden):
        pass

    def close(self):
        pass

    def wait(self):
        pass

    def focus(self):
        pass


class Dialog(Window):

    def __init__(self, bananawidget, parentwindow, title):
        super().__init__(bananawidget, title)
