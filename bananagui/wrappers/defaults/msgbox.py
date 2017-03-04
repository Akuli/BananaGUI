from bananagui import Orient, widgets


def message(icon, parentwindow, message, title, buttons, defaultbutton):
    # TODO: do something with the icon?
    def on_click(text):
        nonlocal result
        result = text
        dialog.close()

    result = None

    dialog = widgets.Dialog(parentwindow, title=title, minimum_size=(350, 150))
    mainbox = widgets.Box()
    dialog.add(mainbox)

    mainbox.append(widgets.Label(text=message))
    buttonbox = widgets.Box(Orient.HORIZONTAL, expand=(True, False))
    mainbox.append(buttonbox)

    focus_this = None
    for buttontext in buttons:
        button = widgets.Button(text=buttontext)
        button.on_click.connect(on_click, buttontext)
        buttonbox.extend([widgets.Dummy(), button, widgets.Dummy()])
        if buttontext == defaultbutton:
            focus_this = button
    if focus_this is not None:
        focus_this.focus()

    dialog.on_close.connect(dialog.close)
    dialog.wait()
    return result


# TODO: font dialog.
