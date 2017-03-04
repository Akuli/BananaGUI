"""BananaGUI hello world test."""

from bananagui import mainloop, widgets


def main():
    window = widgets.Window("Hello World!")
    window.add(widgets.Label("Hello World!"))
    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
