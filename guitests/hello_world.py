"""BananaGUI hello world test."""

import bananagui


def main():
    window = bananagui.Window("Hello World!", bananagui.Label("Hello World!"))
    window.on_close.connect(bananagui.mainloop.quit)
    bananagui.mainloop.run()


if __name__ == '__main__':
    main()
