import functools

# We can't import bananagui.gui now because bananagui.gui may import
# this, but bananagui.gui will be accessible through the bananagui
# module when it's imported.
import bananagui


def _on_click(dialog, event):
    dialog.response = event.widget['text']
    dialog.destroy()


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
