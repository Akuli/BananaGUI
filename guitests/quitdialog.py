from bananagui import gui


def on_destroy(event):
    answer = gui.questiondialog(
        event.widget, "Do you really want to quit?",
        buttons=["Yes", "No"])
    if answer == "Yes":
        gui.quit()


def main():
    with gui.Window(title="Quit dialog test") as window:
        label = gui.Label(window, text="Close me!")
        window['child'] = label

        # The first callback destroys the window when its close button
        # is clicked.
        del window['on_destroy'][0]
        window['on_destroy'].append(on_destroy)

        gui.main()


if __name__ == '__main__':
    main()
