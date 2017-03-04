"""BananaGUI size test."""

from bananagui import mainloop, widgets

instructions = ("The window should always fully show\n"
                "this text and the button you clicked.")


def on_click(label, button):
    if button.text == "Hide instructions":
        label.text = 'hidden'
        button.text = "Show instructions"
    else:
        label.text = instructions
        button.text = "Hide instructions"


def main():
    # minimum_size=(1, 1) tests if setting it on initialization makes
    # a difference (it shouldn't).
    window = widgets.Window("Minimum size test", minimum_size=(1, 1))
    box = widgets.Box()
    window.add(box)

    label = widgets.Label('hidden')
    box.append(label)
    button = widgets.Button("Show instructions")
    button.on_click.connect(on_click, label, button)
    box.append(button)

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
