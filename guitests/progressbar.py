import functools

import bananagui
from bananagui import gui


def set_progress(progressbar, event):
    progressbar['progress'] = event.widget['value'] / 100


def main():
    with gui.Window(title="Scrollbar test") as window:
        box = gui.Box.vertical(window)
        window['child'] = box

        progressbar = gui.Progressbar(
            box, orientation=bananagui.HORIZONTAL, expand=(True, False))
        box['children'].append(progressbar)

        box['children'].append(gui.Dummy(box))

        spinbox = gui.Spinbox(box, valuerange=range(101), expand=(True, False))
        spinbox['value.changed'].append(functools.partial(set_progress, progressbar))
        box['children'].append(spinbox)

        window['on_destroy'].append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
