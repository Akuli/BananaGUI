import os
import pprint

from bananagui import mainloop, iniloader


def click(button):
    print("You clicked me!")


def main():
    with open(os.path.join('guitests', 'testgui.ini'), 'r') as f:
        widgetdict = iniloader.load(f)
    pprint.pprint(widgetdict)
    widgetdict['button'].on_click.connect(click)
    with widgetdict['window'] as window:
        window.on_close.connect(mainloop.quit)
        mainloop.run()


if __name__ == '__main__':
    main()
