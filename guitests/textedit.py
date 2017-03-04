"""BananaGUI TextEdit test."""

from bananagui import Orient, mainloop, widgets


def text_changed(textedit):
    print("text changed to", repr(textedit.text))


def clear(textview):
    textview.text = ''


def add_text(textedit):
    textedit.text += " Click!"


def main():
    window = widgets.Window("TextEdit test", minimum_size=(300, 200))

    bigbox = widgets.Box()
    window.add(bigbox)

    textedit = widgets.TextEdit("Enter something...")
    textedit.on_text_changed.connect(text_changed, textedit)
    bigbox.append(textedit)

    buttonbox = widgets.Box(Orient.HORIZONTAL, expand=(True, False))
    bigbox.append(buttonbox)

    addbutton = widgets.Button("Add text")
    addbutton.on_click.connect(add_text, textedit)
    buttonbox.append(addbutton)

    clearbutton = widgets.Button("Clear")
    clearbutton.on_click.connect(clear, textedit)
    buttonbox.append(clearbutton)

    selectallbutton = widgets.Button("Select all")
    selectallbutton.on_click.connect(textedit.select_all)
    buttonbox.append(selectallbutton)

    focusbutton = widgets.Button("Focus")
    focusbutton.on_click.connect(textedit.focus)
    buttonbox.append(focusbutton)

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
