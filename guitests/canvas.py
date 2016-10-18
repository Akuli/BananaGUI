import bananagui
from bananagui import gui


def main():
    with gui.Window(title="Canvas test") as window:
        canvas = gui.Canvas(window, minimum_size=(400, 400))
        window['child'] = canvas

        canvas.draw_line((100, 100), (200, 100))
        canvas.draw_polygon((100, 100), (100, 200), (200, 200),
                            fillcolor=bananagui.RED, linecolor=bananagui.BLUE,
                            linethickness=3)
        canvas.draw_oval((300, 300), 200, 100, fillcolor=bananagui.CYAN,
                         linecolor=bananagui.ORANGE, linethickness=5)
        canvas.draw_circle((300, 300), 50, fillcolor=bananagui.ORANGE,
                           linecolor=bananagui.RED, linethickness=10)

        window['on_destroy'].append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
