import enum


class Orient(enum.IntEnum):
    HORIZONTAL = 1
    VERTICAL = 2


class Align(enum.IntEnum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3

    # These are aliases because LEFT and RIGHT are used more often.
    TOP = LEFT
    BOTTOM = RIGHT


# This is not 0 or 1 because returning True or False from a callback
# must not be allowed. I don't think an enum with just one value is
# worth it, so this is just an integer. The callbacks can also return
# None if they are not supposed to run again.
RUN_AGAIN = object()
