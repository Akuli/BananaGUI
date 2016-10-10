from bananagui import gui


def main():
    window = gui.Window(title="Separator test")

    bigbox = gui.Box.vertical(window)
    window['child'] = bigbox

    toplabel = gui.Label(bigbox, text="Top")
    bigbox.append(toplabel)

    bigbox.append(gui.Separator.horizontal(bigbox))

    bottombox = gui.Box.horizontal(bigbox)
    bigbox.append(bottombox)

    bottomleftlabel = gui.Label(bottombox, text="Bottom left")
    bottombox.append(bottomleftlabel)

    bottombox.append(gui.Separator.vertical(bottombox))

    bottomrightlabel = gui.Label(bottombox, text="Bottom right")
    bottombox.append(bottomrightlabel)

    window['destroyed.changed'].append(gui.quit)
    gui.main()


if __name__ == '__main__':
    main()
