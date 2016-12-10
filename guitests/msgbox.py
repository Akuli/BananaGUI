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

from bananagui import color, mainloop, msgbox, widgets


class DialogTest(widgets.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        box = widgets.Box.vertical(self)
        self.child = box

        infobutton = widgets.Button(box, "Info")
        infobutton.on_click.append(self.info)
        box.append(infobutton)

        warningbutton = widgets.Button(box, "Warning")
        warningbutton.on_click.append(self.warning)
        box.append(warningbutton)

        errorbutton = widgets.Button(box, "Error")
        errorbutton.on_click.append(self.error)
        box.append(errorbutton)

        questionbutton = widgets.Button(box, "Question")
        questionbutton.on_click.append(self.question)
        box.append(questionbutton)

        colorbutton = widgets.Button(box, "Choose a color...")
        colorbutton.on_click.append(self.choose_color)
        box.append(colorbutton)

    def info(self, infobutton):
        result = msgbox.info(self, "Information!")
        print(repr(result))

    def warning(self, warningbutton):
        result = msgbox.warning(
            self, "Warning!", title="Be warned!",
            buttons=["What's going to happen next?"])
        print(repr(result))

    def error(self, errorbutton):
        result = msgbox.error(
            self, "Error!", title="Oh no!",
            buttons=["I'm screwed!", "I'm not screwed"],
            defaultbutton="I'm screwed!")
        print(repr(result))

    def question(self, questionbutton):
        result = msgbox.question(
            self, "Do you like BananaGUI?",
            buttons=["Yes", "No"], defaultbutton="Yes")
        print(repr(result))

    def choose_color(self, colorbutton):
        result = msgbox.colordialog(self, defaultcolor=color.RED,
                                    title="Choose a color")
        print(repr(result))

    # TODO: font dialog


def close_callback(window):
    result = msgbox.question(
        window, "Do you really want to quit?", title="Quit?",
        buttons=["Yes", "No"], defaultbutton="Yes")
    print(repr(result))
    if result == "Yes":
        mainloop.quit()


def main():
    with DialogTest("Dialog test") as window:
        del window.on_close[0]     # The default handler.
        window.on_close.append(close_callback)
        mainloop.run()


if __name__ == '__main__':
    main()
