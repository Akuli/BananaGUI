import bananagui


def click_callback():
    print("clicked")

window = bananagui.Window("Hello World!")

button = bananagui.Button("Click me")
button.on_click.connect(click_callback)
window.add(button)

window.on_close.connect(bananagui.quit)
bananagui.run()
