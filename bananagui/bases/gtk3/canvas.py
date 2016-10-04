class Canvas:

    def __init__(self, parent):
        raise NotImplementedError  # TODO
        super().__init__(parent)

    def _bananagui_set_size(self, size):
        ...

    def _bananagui_set_background(self, background):
        ...

    def draw_line(self, pos1, pos2, thickness, color):
        ...

    def draw_polygon(self, *positions, fillcolor, linecolor, linethickness):
        ...

    def draw_oval(self, centerpos, xradius, yradius, fillcolor,
                  linecolor, linethickness):
        ...
