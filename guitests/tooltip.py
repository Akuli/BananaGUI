import bananagui


window = bananagui.Window("Tooltip test")
label = bananagui.Label("Test Label", tooltip="Test Tooltip")
window.add(label)

window.on_close.connect(bananagui.mainloop.quit)
bananagui.mainloop.run()
