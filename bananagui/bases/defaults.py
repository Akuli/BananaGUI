import functools

# We can't import bananagui.gui now because bananagui.gui may import
# this, but bananagui.gui will be accessible through the bananagui
# module when it's imported.
import bananagui


def _on_click(dialog, event):
    dialog.response = event.widget['text']
    dialog.destroy()


def _messagedialog(parentwindow, message, title, buttons, defaultbutton):
    gui = bananagui.gui

    dialog = gui.Dialog(parentwindow, title=title, minimum_size=(350, 150))

    mainbox = gui.Box.vertical(dialog)
    dialog['child'] = mainbox

    label = gui.Label(mainbox, text=message)
    mainbox['children'].append(label)

    buttonbox = gui.Box.horizontal(mainbox, expand=(True, False))
    for buttontext in buttons:
        button = gui.Button(buttonbox, text=buttontext)
        button['on_click'].append(functools.partial(_on_click, dialog))
        buttonbox['children'].extend([
            gui.Dummy(buttonbox), button, gui.Dummy(buttonbox)])
    mainbox['children'].append(buttonbox)

    dialog.response = None  # This is not special for BananaGUI in any way.
    dialog.wait()
    return dialog.response


# TODO: support icons?
infodialog = warningdialog = errordialog = questiondialog = _messagedialog


def fontdialog(parentwindow, default, title):
    raise NotImplementedError("TODO")
# flake8: noqa

from .dialogs import (infodialog, warningdialog, errordialog,
                      questiondialog, fontdialog)
from .spinner import Spinner
import collections
import math

# We can only import modules from bananagui.gui because this file can be
# loaded by bananagui.gui.__init__.
import bananagui
from bananagui.gui import canvas, timeouts


_LINES = 15
_DELAY = 60


class Spinner:

    def __init__(self, parent, **kwargs):
        self.__widget = canvas.Canvas(parent, minimum_size=(25, 25))
        self.real_widget.raw_set(self.__widget['real_widget'])
        self.__positions = collections.deque()
        for i in range(_LINES):
            #          /|
            #         / |
            #        /  |
            #       /   |
            #      /    |
            #   1 /     | y
            #    /      |
            #   /       |
            #  / angle  |
            # /_)_______|
            #     x
            #
            # sin(angle) = y / 1  =>  y = sin(angle)
            # cos(angle) = x / y  =>  x = cos(angle)
            angle = 360 * i // _LINES
            y = math.sin(math.radians(angle))
            x = math.cos(math.radians(angle))
            self.__positions.append((x, y))
        super().__init__(parent, **kwargs)

    def __draw(self):
        self.__widget.clear()

        if not self['spinning']:
            # We're not spinning anymore.
            return None

        width, height = self.__widget['size']
        diameter = min(width, height)

        # Rotating by a positive number would make the spinner spin
        # counter-clockwise.
        self.__positions.rotate(-1)

        for index, (x, y) in enumerate(self.__positions):
            brightness = index * 255 // _LINES
            start = (x * diameter // 5 + width // 2,
                     y * diameter // 5 + height // 2)
            end = (x * diameter // 2 + width // 2,
                   y * diameter // 2 + height // 2)
            thickness = max(diameter // 10, 1)
            color = bananagui.Color(brightness, brightness, brightness)
            self.__widget.draw_line(start, end, thickness=thickness,
                                    color=color)

        # Keep spinning.
        return bananagui.RUN_AGAIN

    def _bananagui_set_spinning(self, spinning):
        if spinning:
            # Start spinning.
            timeouts.add_timeout(_DELAY, self.__draw)
        # We don't need an else because __draw knows when to stop.
