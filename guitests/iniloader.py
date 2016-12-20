import os
import pprint

from bananagui import mainloop, iniloader

filename = os.path.join('guitests', 'data', 'testgui.ini')


def click(button):
    print("Click!")


def main():
    with open(filename, 'r') as f:
        the_widgets = iniloader.load_ini(f)
    pprint.pprint(the_widgets)
    with the_widgets['window']:
        the_widgets['button'].on_click.append(click)
        the_widgets['window'].on_close.append(mainloop.quit)
        mainloop.run()


if __name__ == '__main__':
    main()
