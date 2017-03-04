import math
import shutil

from bananagui import font


def print_table(thinglist):
    """Print a list of strings as a nice table."""
    maxlen = max(map(len, thinglist))
    columns = shutil.get_terminal_size().columns // (maxlen + 2)
    if columns < 2:
        for thing in thinglist:
            print(thing)
    else:
        rows = math.ceil(len(thinglist) / columns)
        for y in range(rows):
            string = '  '.join(item.ljust(maxlen)
                               for item in thinglist[y::rows])
            print(string.rstrip())


def main():
    families = sorted(font.get_families())
    print_table(families)


if __name__ == '__main__':
    main()
