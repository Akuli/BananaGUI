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

import functools

from bananagui import widgets


def _on_click(dialog, button):
    dialog.response = button.text
    dialog.close()


def _messagedialog(parentwindow, message, title, buttons, defaultbutton):
    dialog = widgets.Dialog(parentwindow, title=title, minimum_size=(350, 150))

    mainbox = widgets.Box.vertical(dialog)
    dialog.child = mainbox

    label = widgets.Label(mainbox, text=message)
    buttonbox = widgets.Box.horizontal(mainbox, expand=(True, False))
    mainbox.extend([label, buttonbox])

    focus_this = None
    for buttontext in buttons:
        button = widgets.Button(buttonbox, text=buttontext)
        callback = functools.partial(_on_click, dialog)
        button.on_click.append(callback)

        # Adding a dummy on both sides will give us more space between
        # the buttons than between the buttons and the window border.
        buttonbox.extend([
            widgets.Dummy(buttonbox), button, widgets.Dummy(buttonbox)])
        if buttontext == defaultbutton:
            focus_this = button

    if focus_this is not None:
        focus_this.focus()

    dialog.response = None  # This is not special for BananaGUI in any way.
    dialog.wait()
    return dialog.response


# TODO: support icons?
info = warning = error = question = _messagedialog


# TODO: font dialog.
