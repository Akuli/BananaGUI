"""Hello world program."""

import gui


gui = gui.get('tkinter')


def click_callback(pressed):
    """The user pressed or released the button."""
    if pressed:
        print("Pressed!")
    else:
        print("Released!")


window = gui.Window()

mainbox = gui.Box.vbox(window)
window.child(mainbox)

topbox = gui.Box.vbox(mainbox)
mainbox.prepend(topbox)

label = gui.Label(topbox)
label.text("Enter something:")
topbox.append(label, expand=True)

button = gui.TextButton(topbox)
button.text("Click me!")
button.pressed.callbacks.append(click_callback)
topbox.append(button)

window.size((200, 200))
window.showing.callbacks.append(gui.quit)
gui.main()
