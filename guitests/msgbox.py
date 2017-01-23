# Copyright (c) 2016-2017 Akuli

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


def info(window):
    result = msgbox.info(window, "Information!")
    print(repr(result))


def warning(window):
    result = msgbox.warning(
        window, "Warning!", title="Be warned!",
        buttons=["What's going to happen next?"])
    print(repr(result))


def error(window):
    result = msgbox.error(
        window, "Error!", title="Oh no!",
        buttons=["I'm screwed!", "I'm not screwed"],
        defaultbutton="I'm screwed!")
    print(repr(result))


def question(window):
    result = msgbox.question(
        window, "Do you like BananaGUI?",
        buttons=["Yes", "No"], defaultbutton="Yes")
    print(repr(result))


def choose_color(window):
    result = msgbox.colordialog(
        window, defaultcolor=color.RED,
        title="Choose a color")
    print(repr(result))


def main():
    window = widgets.Window("Dialog test")
    box = widgets.Box()
    window.add(box)

    texts = ["Info", "Warning", "Error", "Question", "Choose a color"]
    functions = [info, warning, error, question, choose_color]
    for text, function in zip(texts, functions):
        button = widgets.Button(text)
        button.on_click.connect(function, window)
        box.append(button)

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
