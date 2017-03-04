from bananagui import Orient, clipboard, mainloop, widgets


def copy_from_entry(entry):
    clipboard.set_text(entry.text)


def paste_to_entry(entry):
    text = clipboard.get_text()
    if text is None:
        print("there's no text on the clipboard")
    else:
        entry.text += text


def main():
    window = widgets.Window("Clipboard test")
    mainbox = widgets.Box()
    window.add(mainbox)

    entry = widgets.Entry(expand=(True, False))
    mainbox.append(entry)

    mainbox.append(widgets.Dummy())

    buttonbox = widgets.Box(Orient.HORIZONTAL, expand=(True, False))
    mainbox.append(buttonbox)

    copybutton = widgets.Button("Copy everything")
    copybutton.on_click.connect(copy_from_entry, entry)
    buttonbox.append(copybutton)

    pastebutton = widgets.Button("Paste to the end")
    pastebutton.on_click.connect(paste_to_entry, entry)
    buttonbox.append(pastebutton)

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
