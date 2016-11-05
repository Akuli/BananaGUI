# Banana GUI :banana:

This is a wrapper around the Python Tkinter and GTK+ 3 bindings. You can
write code using BananaGUI, and then run the same code using any of
these toolkits. BananaGUI may feature PyQt5 support later.

## Hello World!

A minimal Hello World program in BananaGUI looks like this:

```py
import bananagui
bananagui.load('.gtk3', '.tkinter')
from bananagui import gui

with gui.Window(title="Hello World") as window:
    window['child'] = gui.Label(window, text="Hello World!")
    window['on_close'].append(gui.quit)
    gui.main()
```

Here's a Hello World with some more features:

```py
import bananagui
bananagui.load('.gtk3', '.tkinter')
from bananagui import gui


def click_callback(event):
    print("You clicked me!")


def quit_callback(event):
    response = gui.questiondialog(
        event.widget, "Are you sure you want to say Goodbye World?",
        title="Goodbye World", buttons=["Yes, Goodbye World!", "No"])
    if response == "Yes, Goodbye World!":
        gui.quit()


def main():
    with gui.Window(title="Hello World 2", size=(300, 120)) as window:
        box = gui.Box.vertical(window)
        window['child'] = box

        label = gui.Label(box, text="Hello World!")
        box['children'].append(label)

        button = gui.Button(box, text="Click me!")
        button['on_click'].append(click_callback)
        box['children'].append(button)

        del window['on_close'][0]  # The default callback.
        window['on_close'].append(quit_callback)
        gui.main()


if __name__ == '__main__':
    main()
```

I don't have good documentation anywhere yet, but calling `help()` on
things should be useful in many places. You can also read the source if
you're wondering something.

## Thanks

I want to thank these people for helping me write BananaGUI:

- [The 8Banana Organization](https://github.com/8Banana)
