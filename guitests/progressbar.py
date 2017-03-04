from bananagui import mainloop, widgets


def set_progress(progressbar, spinbox):
    progressbar.progress = spinbox.value / 100
    print(progressbar)


def set_bouncing(bouncingbar, checkbox):
    bouncingbar.bouncing = checkbox.checked
    print(bouncingbar)


def main():
    window = widgets.Window("Progress bar test")
    box = widgets.Box()
    window.add(box)

    progressbar = widgets.Progressbar(expand=(True, False))
    box.append(progressbar)

    spinbox = widgets.Spinbox(valuerange=range(101), expand=(True, False))
    spinbox.on_value_changed.connect(set_progress, progressbar, spinbox)
    box.append(spinbox)

    box.append(widgets.Dummy())

    bouncingbar = widgets.BouncingProgressbar(expand=(True, False))
    box.append(bouncingbar)

    checkbox = widgets.Checkbox("Bouncing", expand=(True, False))
    checkbox.on_checked_changed.connect(
        set_bouncing, bouncingbar, checkbox)
    box.append(checkbox)

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
