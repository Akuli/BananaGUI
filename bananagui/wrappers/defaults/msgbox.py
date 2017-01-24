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

import bananagui
from bananagui import widgets


def message(icon, parentwindow, message, title, buttons, defaultbutton):
    # TODO: do something with the icon?
    def done(text):
        nonlocal result
        result = text
        dialog.close()

    dialog = widgets.Dialog(parentwindow, title=title, minimum_size=(350, 150))

    mainbox = widgets.Box()
    dialog.add(mainbox)

    mainbox.append(widgets.Label(text=message))
    buttonbox = widgets.Box(bananagui.HORIZONTAL, expand=(True, False))
    mainbox.append(buttonbox)

    focus_this = None
    for buttontext in buttons:
        button = widgets.Button(text=buttontext)
        button.on_click.connect(done, buttontext)
        buttonbox.extend([widgets.Dummy(), button, widgets.Dummy()])
        if buttontext == defaultbutton:
            focus_this = button
    if focus_this is not None:
        focus_this.focus()

    dialog.on_close.connect(done, None)
    dialog.wait()
    return result   # noqa


# TODO: font dialog.
