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

# We can't import bananagui.gui now because bananagui.gui may import
# this, but bananagui.gui will be accessible through the bananagui
# module when it's imported.
import bananagui


def _on_click(dialog, event):
    dialog.response = event.widget['text']
    dialog.close()


def _messagedialog(parentwindow, message, title, buttons, defaultbutton):
    gui = bananagui.gui

    dialog = gui.Dialog(parentwindow, title=title, minimum_size=(350, 150))

    mainbox = gui.Box.vertical(dialog)
    dialog['child'] = mainbox

    label = gui.Label(mainbox, text=message)
    mainbox['children'].append(label)

    buttonbox = gui.Box.horizontal(mainbox, expand=(True, False))
    for buttontext in buttons:
        button = gui.Button(buttonbox, text=buttontext)
        button['on_click'].append(functools.partial(_on_click, dialog))
        buttonbox['children'].extend([
            gui.Dummy(buttonbox), button, gui.Dummy(buttonbox)])
    mainbox['children'].append(buttonbox)

    dialog.response = None  # This is not special for BananaGUI in any way.
    dialog.wait()
    return dialog.response


# TODO: support icons?
infodialog = warningdialog = errordialog = questiondialog = _messagedialog


def fontdialog(parentwindow, default, title):
    raise NotImplementedError("TODO")
