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

import bananagui
from bananagui import gui


class DialogTest(gui.Window):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        box = gui.Box.vertical(self)
        self.child = box

        infobutton = gui.Button(box, text="Info")
        infobutton.on_click.append(self.info)
        box.append(infobutton)

        warningbutton = gui.Button(box, text="Warning")
        warningbutton.on_click.append(self.warning)
        box.append(warningbutton)

        errorbutton = gui.Button(box, text="Error")
        errorbutton.on_click.append(self.error)
        box.append(errorbutton)

        questionbutton = gui.Button(box, text="Question")
        questionbutton.on_click.append(self.question)
        box.append(questionbutton)

        colorbutton = gui.Button(box, text="Choose a color...")
        colorbutton.on_click.append(self.choose_color)
        box.append(colorbutton)


    def info(self, infobutton):
        result = gui.infodialog(self, "Information!")
        print(repr(result))

    def warning(self, warningbutton):
        result = gui.warningdialog(self, "Warning!", title="Be warned!",
                                   buttons=["What's going to happen next?"])
        print(repr(result))

    def error(self, errorbutton):
        result = gui.errordialog(
            self, "Error!", title="Oh no!",
            buttons=["I'm screwed!", "I'm not screwed"],
            defaultbutton="I'm screwed!")
        print(repr(result))

    def question(self, questionbutton):
        result = gui.questiondialog(
            self, "Do you like BananaGUI?",
            buttons=["Yes", "No"], defaultbutton="Yes")
        print(repr(result))

    def choose_color(self, colorbutton):
        result = gui.colordialog(self, defaultcolor=bananagui.RED,
                                 title="Choose a color")
        print(repr(result))

    # TODO: font dialog


def close_callback(window):
    result = gui.questiondialog(
        window, "Do you really want to quit?", title="Quit?",
        buttons=["Yes", "No"], defaultbutton="Yes")
    print(repr(result))
    if result == "Yes":
        gui.quit()


def main():
    with DialogTest(title="Dialog test") as window:
        del window.on_close[0]  # The default handler.
        window.on_close.append(close_callback)
        gui.main()


if __name__ == '__main__':
    main()
