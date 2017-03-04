"""BananaGUI label align test."""

from bananagui import Align, mainloop, widgets


def main():
    window = widgets.Window("Label align test")
    box = widgets.Box()
    window.add(box)

    names = ['left', 'center', 'right']
    aligns = [Align.LEFT, Align.CENTER, Align.RIGHT]
    for name, align in zip(names, aligns):
        label = widgets.Label("this is aligned to\n" + name, align=align)
        box.append(label)

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
