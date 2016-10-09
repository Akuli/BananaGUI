import sys

from bananagui import color, gui


def main():
    with gui.Window(title="Canvas test") as window:
        canvas = gui.Canvas(window, size=(400, 400))
        window['child'] = canvas

        canvas.draw_line((100, 100), (200, 100))
        canvas.draw_polygon((100, 100), (100, 200), (200, 200),
                            fillcolor=color.RED, linecolor=color.BLUE,
                            linethickness=3)
        canvas.draw_oval((300, 300), 200, 100, fillcolor=color.CYAN,
                         linecolor=color.ORANGE, linethickness=5)
        canvas.draw_circle((300, 300), 50, fillcolor=color.ORANGE,
                           linecolor=color.RED, linethickness=10)

        window.destroyed.changed.connect(gui.quit)
        sys.exit(gui.main())


if __name__ == '__main__':
    main()
