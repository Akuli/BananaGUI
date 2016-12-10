# BananaGUI :banana:

This is a wrapper around the Python Tkinter and GTK+ 3 bindings. You can
write code using BananaGUI, and then run the same code using any of
these toolkits. BananaGUI may feature PyQt5 support later.

## Hello World!

A minimal Hello World program in BananaGUI looks like this:

```py
import bananagui
from bananagui import mainloop, widgets

bananagui.load('.tkinter')
with widgets.Window("Hello World") as window:
    window.child = widgets.Label(window, "Hello World!")
    window.on_close.append(mainloop.quit)
    mainloop.run()
```

Here's a Hello World with some more features:

```py
import bananagui
from bananagui import mainloop, msgbox, widgets


def click_callback(button):
    print("You clicked me!")


def quit_callback(window):
    response = msgbox.question(
        window, "Are you sure you want to say Goodbye World?",
        title="Goodbye World", buttons=["Yes, Goodbye World!", "No"])
    if response == "Yes, Goodbye World!":
        mainloop.quit()


def main():
    bananagui.load('.tkinter')
    with widgets.Window("Hello World 2", size=(300, 120)) as window:
        box = widgets.Box.vertical(window)
        window.child = box

        label = widgets.Label(box, "Hello World!")
        box.append(label)

        button = widgets.Button(box, "Click me!")
        button.on_click.append(click_callback)
        box.append(button)

        del window.on_close[0]  # Delete the default callback.
        window.on_close.append(quit_callback)
        mainloop.run()


if __name__ == '__main__':
    main()
```

You can also write your GUI using the .ini format and then load it with
`bananagui.iniloader`:

```py
import bananagui
from bananagui import iniloader, mainloop


# Usually this would be in another file.
INI = """\
[window]
class = widgets.Window
title = "Hello World 3"
child = label

[label]
class = widgets.Label
parent = window
text = "Hello World!"
"""


def main():
    bananagui.load('.tkinter')
    widgets = iniloader.load_ini(INI)
    # Now widgets is a dictionary.
    with widgets['window'] as window:
        window.on_close.append(mainloop.quit)
        mainloop.run()


if __name__ == '__main__':
    main()
```

See [the guitests directory](guitests) for more examples.

I don't have good documentation anywhere yet, but calling `help()` on
things should be useful in many places. You can also read the source if
you're wondering something.

## Thanks

I want to thank these people for helping me write BananaGUI:

- [The 8Banana Organization](https://github.com/8Banana)
