"""BananaGUI checkbox test."""

from bananagui import mainloop, widgets


def do_check(checkbox):
    if checkbox.checked:
        checkbox.text = "Uncheck me!"
    else:
        checkbox.text = "Check me!"
    print(checkbox)


def main():
    window = widgets.Window("Checkbox test")
    checkbox = widgets.Checkbox("Check me!")
    checkbox.on_checked_changed.connect(do_check, checkbox)
    window.add(checkbox)
    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
