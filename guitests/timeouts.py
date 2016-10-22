import itertools

import bananagui
from bananagui import gui


def once():
    print("I run once.")


def over_and_over():
    number = next(counter)
    print("I have ran %d times before." % number)
    if number >= 5:
        print("It's time to stop now.")
        gui.quit()
        return None
    return bananagui.RUN_AGAIN

counter = itertools.count()


def main():
    gui.add_timeout(500, once)
    gui.add_timeout(1000, over_and_over)
    gui.main()


if __name__ == '__main__':
    main()
