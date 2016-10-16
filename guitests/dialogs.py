import bananagui
from bananagui import gui


class DialogTestWindow(gui.Window):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        box = gui.Box.vertical(self)
        self['child'] = box

        colorbutton = gui.Button(box, text="Choose a color...")
        colorbutton['on_click'].append(self.choose_color)
        box.append(colorbutton)

    def choose_color(self, event):
        result = gui.colordialog(self, default=bananagui.RED,
                                 title="Choose a color")
        print(result)


def main():
    with DialogTestWindow(title="Dialog test") as window:
        window['on_destroy'].append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
