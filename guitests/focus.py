"""Focusing GUI test."""

from bananagui import mainloop, widgets


def on_click(other_button):
    other_button.focus()


def main():
    message = ("Press tab and then enter. The focus\n"
               "should move to the other button.")

    window = widgets.Window("Focus test", minimum_size=(250, 150))
    box = widgets.Box()
    window.add(box)

    label = widgets.Label(message)
    box.append(label)

    button1 = widgets.Button("Focus the button below")
    button2 = widgets.Button("Focus the button above")
    button1.on_click.connect(on_click, button2)
    button2.on_click.connect(on_click, button1)
    box.extend([button1, button2])

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
