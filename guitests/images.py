"""BananaGUI test for widgets that use images."""

import os

from bananagui import Orient, images, mainloop, widgets


def main():
    window = widgets.Window("Image test")
    image = images.Image(os.path.join('guitests', 'banana.png'))

    box = widgets.Box(Orient.HORIZONTAL)
    window.add(box)

    label = widgets.ImageLabel(image)
    box.append(label)

    button = widgets.ImageButton(image)
    button.on_click.connect(print, button)
    box.append(button)

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
