from bananagui import Orient, mainloop, widgets


def value_changed(called_widget, *other_widgets):
    for widget in other_widgets:
        # This doesn't recurse too much because changed callbacks
        # don't run if the old and new value are equal.
        widget.value = called_widget.value


def main():
    values = range(0, 51, 5)

    window = widgets.Window("Slider test", minimum_size=(300, 200))
    mainbox = widgets.Box(Orient.HORIZONTAL)
    window.add(mainbox)

    left_side = widgets.Box()
    hslider = widgets.Slider(values, expand=(True, False))
    spinbox = widgets.Spinbox(values, expand=(True, False))
    left_side.extend([
        widgets.Dummy(), hslider,
        widgets.Dummy(), spinbox,
        widgets.Dummy()])
    mainbox.append(left_side)

    vslider = widgets.Slider(values, Orient.VERTICAL)
    mainbox.append(vslider)

    # Python's sets are awesome.
    all_widgets = {hslider, vslider, spinbox}
    for this in all_widgets:
        others = all_widgets - {this}
        this.on_value_changed.connect(value_changed, this, *others)

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
