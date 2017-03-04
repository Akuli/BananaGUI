import os
import pprint

from bananagui import mainloop, iniloader


def main():
    with open(os.path.join('guitests', 'testgui.ini'), 'r') as f:
        widgetdict = iniloader.load(f)
    pprint.pprint(widgetdict)
    widgetdict['button'].on_click.connect(print, "You clicked me!")
    widgetdict['window'].on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
