from bananagui import mainloop, widgets


def main():
    window = widgets.Window("Tooltip test")

    box = widgets.Box()
    window.add(box)

    toplabel = widgets.Label("Top label!", tooltip="Top label tooltip!")
    bottomlabel = widgets.Label("Bottom label!",
                                tooltip="Bottom label tooltip!")
    box.extend([toplabel, bottomlabel])
    print(toplabel)
    print(bottomlabel)

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
