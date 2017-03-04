from bananagui import Orient, mainloop, widgets


def main():
    window = widgets.Window("Separator test")

    bigbox = widgets.Box()
    window.add(bigbox)

    toplabel = widgets.Label("Top")
    bigbox.append(toplabel)
    hsep = widgets.Separator()
    bigbox.append(hsep)
    print(hsep)
    bottombox = widgets.Box(Orient.HORIZONTAL)
    bigbox.append(bottombox)

    bottombox.append(widgets.Label("Bottom left"))
    vsep = widgets.Separator(Orient.VERTICAL)
    bottombox.append(vsep)
    print(vsep)
    bottombox.append(widgets.Label("Bottom right"))

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
