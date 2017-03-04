from bananagui import color, mainloop, msgbox, widgets


def info(window):
    result = msgbox.info(window, "Information!", ["Got it"])
    print(repr(result))


def warning(window):
    result = msgbox.warning(
        window, "Be careful!", ["What's going to happen if I'm not?"],
        title="Warning")
    print(repr(result))


def error(window):
    result = msgbox.error(
        window, "Oh no!", ["I'm screwed!", "I'm not screwed"],
        defaultbutton="I'm screwed!", title="Error")
    print(repr(result))


def question(window):
    result = msgbox.question(
        window, "Do you like BananaGUI?", ["Yes", "No"],
        defaultbutton="Yes")
    print(repr(result))


def choose_color(window):
    result = msgbox.colordialog(
        window, defaultcolor=color.RED,
        title="Choose a color")
    print(repr(result))


def main():
    window = widgets.Window("Message box test")
    box = widgets.Box()
    window.add(box)

    texts = ["Info", "Warning", "Error", "Question", "Choose a color"]
    functions = [info, warning, error, question, choose_color]
    for text, function in zip(texts, functions):
        button = widgets.Button(text)
        button.on_click.connect(function, window)
        box.append(button)

    window.on_close.connect(mainloop.quit)
    mainloop.run()


if __name__ == '__main__':
    main()
