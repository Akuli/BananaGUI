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

from .containers import Bin


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
