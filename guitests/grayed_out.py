import bananagui


window = bananagui.Window("Annoying Button")
window.add(bananagui.Button("Haha, you can't click me!", grayed_out=True))
window.on_close.connect(bananagui.quit)
bananagui.run()
