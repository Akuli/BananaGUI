from bananagui import gui


def main():
    window = gui.Window(title="Separator test")

    bigbox = gui.Box.vertical(window)
    window['child'] = bigbox

    toplabel = gui.Label(bigbox, text="Top")
    bigbox['children'].append(toplabel)

    bigbox['children'].append(gui.Separator.horizontal(bigbox))

    bottombox = gui.Box.horizontal(bigbox)
    bigbox['children'].append(bottombox)

    bottomleftlabel = gui.Label(bottombox, text="Bottom left")
    bottombox['children'].append(bottomleftlabel)

    bottombox['children'].append(gui.Separator.vertical(bottombox))

    bottomrightlabel = gui.Label(bottombox, text="Bottom right")
    bottombox['children'].append(bottomrightlabel)

    window['on_destroy'].append(gui.quit)
    gui.main()


if __name__ == '__main__':
    main()
