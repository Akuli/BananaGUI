"""BananaGUI Group widget test."""

import pprint

from bananagui import mainloop, widgets


def main():
    window = widgets.Window("Group test")

    box = widgets.Box()
    window.add(box)

    for number in (1, 2):
        label = widgets.Label("This label is in Group %d!" % number)
        box.append(widgets.Group("Group %d" % number, label))
    pprint.pprint(box[:])

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
