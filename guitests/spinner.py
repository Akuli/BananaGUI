"""BananaGUI spinner test."""

from bananagui import gui


class SpinnerWindow(gui.Window):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        mainbox = gui.Box.vertical(self)
        self['child'] = mainbox

        self.spinner = gui.Spinner(mainbox)
        mainbox.append(self.spinner)

        buttonbox = gui.Box.horizontal(mainbox, expand=(True, False))
        mainbox.append(buttonbox)

        startbutton = gui.Button(buttonbox, text="Start",
                                 on_click=[self.start])
        buttonbox.append(startbutton)

        stopbutton = gui.Button(buttonbox, text="Stop",
                                on_click=[self.stop])
        buttonbox.append(stopbutton)

    def start(self, widget):
        self.spinner['spinning'] = True

    def stop(self, widget):
        self.spinner['spinning'] = False


def main():
    with SpinnerWindow(title="Spinner window") as window:
        window['destroyed.changed'].append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
