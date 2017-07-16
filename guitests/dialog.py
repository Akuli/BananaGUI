import bananagui


def show_dialog():
    dialog = bananagui.Dialog(window)

    button = bananagui.Button("Close me")
    button.on_click.connect(dialog.close)
    dialog.add(button)

    dialog.wait()


window = bananagui.Window("Dialog Test")
button = bananagui.Button("Show the dialog")
button.on_click.connect(show_dialog)
window.add(button)

window.on_close.connect(bananagui.quit)
bananagui.run()
