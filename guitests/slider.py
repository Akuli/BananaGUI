from bananagui import gui


class SliderWindow(gui.Window):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        box = gui.Box.vertical(self)
        self['child'] = box

        values = range(0, 51, 5)

        self.hslider = gui.Slider.horizontal(box, valuerange=values)
        self.hslider['value.changed'].append(self.value_changed)
        box['children'].append(self.hslider)

        self.vslider = gui.Slider.vertical(box, valuerange=values)
        self.vslider['value.changed'].append(self.value_changed)
        box['children'].append(self.vslider)

        self.spinbox = gui.Spinbox(box, valuerange=values)
        self.spinbox['value.changed'].append(self.value_changed)
        box['children'].append(self.spinbox)

    def value_changed(self, event):
        event.widget == self.hslider and print("hi", event.old_value, '->', event.new_value)
        # Python's sets are awesome.
        all_widgets = {self.hslider, self.vslider, self.spinbox}
        other_widgets = all_widgets - {event.widget}
        for widget in other_widgets:
            widget['value'] = event.new_value


def main():
    with SliderWindow(title="Hello World!") as window:
        window['on_destroy'].append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
