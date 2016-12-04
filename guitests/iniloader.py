import os
import pprint

from bananagui import mainloop, widgets, iniloader


def click(button):
    print("Click!")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'testgui.ini'), 'r') as f:
        widgets = iniloader.load_ini(f)
    pprint.pprint(widgets)
    with widgets['window']:
        widgets['button'].on_click.append(click)
        widgets['window'].on_close.append(mainloop.quit)
        mainloop.run()


if __name__ == '__main__':
    main()
