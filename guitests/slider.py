from bananagui import gui


class SliderWindow(gui.Window):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        box = gui.Box.vertical(self)
        self['child'] = box

        # All of these widgets take these keyword arguments.
        kwargs = {'minimum': 0, 'maximum': 50, 'step': 5}

        self.hslider = gui.Slider.horizontal(box, **kwargs)
        self.hslider['value.changed'].append(self.value_changed)
        box.append(self.hslider)

        self.vslider = gui.Slider.vertical(box, **kwargs)
        self.vslider['value.changed'].append(self.value_changed)
        box.append(self.vslider)

        self.spinbox = gui.Spinbox(box, **kwargs)
        self.spinbox['value.changed'].append(self.value_changed)
        box.append(self.spinbox)

    def value_changed(self, event):
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
