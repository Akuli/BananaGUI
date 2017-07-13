import bananagui

window = bananagui.Window("Hello World!", bananagui.Label("Hello World!"))
window.on_close.connect(bananagui.mainloop.quit)
bananagui.mainloop.run()
