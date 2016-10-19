import functools
import os
import sys

try:
    import faulthandler
    faulthandler.enable()
except ImportError:
    pass

sys.path.append('BananaGUI')
import bananagui
bananagui.load(os.environ['base'])
from bananagui import gui


def _on_click(dialog, event):
    dialog.response = event.widget['text']
    dialog.destroy()


def messagebox(parentwindow, message, title, buttons, defaultbutton):
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


if __name__ == '__main__':
    w = gui.Window(title="main window lol", showing=False)
    buttons = ['lol']
    for i in range(4):
        buttons.append(buttons[-1] + 'ol')
    a = messagebox(w, "hello there\ntest", "this is the title",
                   buttons, None)
    print(repr(a))
    gui.quit()
