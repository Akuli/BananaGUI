import collections
import math

# We can only import modules from bananagui.gui because this file can be
# loaded by bananagui.gui.__init__.
from bananagui import Color
from bananagui.gui.canvas import Canvas
from bananagui.gui.timeouts import add_timeout, RUN_AGAIN


_LINES = 15
_DELAY = 60


class Spinner:

    def __init__(self, parent, **kwargs):
        self.__widget = Canvas(parent, minimum_size=(25, 25))
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
            color = Color(brightness, brightness, brightness)
            self.__widget.draw_line(start, end, thickness=thickness,
                                    color=color)

        # Keep spinning.
        return RUN_AGAIN

    def _bananagui_set_spinning(self, spinning):
        if spinning == self['spinning']:
            # We are already spinning or not spinning as the user wants
            # to, no need to do anything.
            return
        if spinning:
            # Start spinning.
            add_timeout(_DELAY, self.__draw)
        # We don't need an else because __draw knows when to stop.
