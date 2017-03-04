"""BananaGUI entry test."""

from bananagui import Orient, mainloop, widgets


def set_grayed_out(entry, checkbox):
    entry.grayed_out = checkbox.checked


def set_secret(entry, checkbox):
    entry.secret = checkbox.checked


def reset_text(entry):
    entry.text = "Enter something..."


def main():
    window = widgets.Window("Entry test")

    entrybox = widgets.Box()
    window.add(entrybox)

    entry = widgets.Entry("Enter something...", expand=(True, False))
    entry.on_text_changed.connect(print, entry)
    entrybox.append(entry)

    entrybox.append(widgets.Dummy())

    buttonbox = widgets.Box(Orient.HORIZONTAL, expand=(True, False))
    entrybox.append(buttonbox)

    resetbutton = widgets.Button("Reset")
    resetbutton.on_click.connect(reset_text, entry)
    buttonbox.append(resetbutton)

    selectallbutton = widgets.Button("Select all")
    selectallbutton.on_click.connect(entry.select_all)
    buttonbox.append(selectallbutton)

    focusbutton = widgets.Button("Focus")
    focusbutton.on_click.connect(entry.focus)
    buttonbox.append(focusbutton)

    grayed = widgets.Checkbox("Grayed out")
    grayed.on_checked_changed.connect(set_grayed_out, entry, grayed)
    buttonbox.append(grayed)

    secret = widgets.Checkbox("Secret")
    secret.on_checked_changed.connect(set_secret, entry, secret)
    buttonbox.append(secret)

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
