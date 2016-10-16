from bananagui import gui


def main():
    window = gui.Window(title="Tooltip test")

    box = gui.Box.vertical(window)
    window['child'] = box

    toplabel = gui.Label(box, text="Top label!",
                         tooltip="Top label tooltip!")
    bottomlabel = gui.Label(box, text="Bottom label!",
                            tooltip="Bottom label tooltip!")
    box['children'].extend([toplabel, bottomlabel])

    window['on_destroy'].append(gui.quit)
    gui.main()


if __name__ == '__main__':
    main()
