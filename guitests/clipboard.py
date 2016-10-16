from bananagui import gui


class ClipboardTestWindow(gui.Window):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        mainbox = gui.Box.vertical(self)
        self['child'] = mainbox

        self.entry = gui.Entry(mainbox, expand=(True, False))
        mainbox.append(self.entry)

        mainbox.append(gui.Dummy(mainbox))

        buttonbox = gui.Box.horizontal(mainbox, expand=(True, False))
        mainbox.append(buttonbox)

        copybutton = gui.Button(buttonbox, text="Copy everything")
        copybutton['on_click'].append(self.copy)
        buttonbox.append(copybutton)

        pastebutton = gui.Button(buttonbox, text="Paste to the end")
        pastebutton['on_click'].append(self.paste)
        buttonbox.append(pastebutton)

    def copy(self, event):
        gui.set_clipboard_text(self.entry['text'])

    def paste(self, event):
        self.entry['text'] += gui.get_clipboard_text()


def main():
    with ClipboardTestWindow(title="Clipboard test") as window:
        window['on_destroy'].append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
