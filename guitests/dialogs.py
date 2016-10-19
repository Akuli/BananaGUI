import bananagui
from bananagui import gui


class DialogTestWindow(gui.Window):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        box = gui.Box.vertical(self)
        self['child'] = box

        infobutton = gui.Button(box, text="Info")
        infobutton['on_click'].append(self.info)
        box['children'].append(infobutton)

        warningbutton = gui.Button(box, text="Warning")
        warningbutton['on_click'].append(self.warning)
        box['children'].append(warningbutton)

        errorbutton = gui.Button(box, text="Error")
        errorbutton['on_click'].append(self.error)
        box['children'].append(errorbutton)

        questionbutton = gui.Button(box, text="Question")
        questionbutton['on_click'].append(self.question)
        box['children'].append(questionbutton)

        colorbutton = gui.Button(box, text="Choose a color...")
        colorbutton['on_click'].append(self.choose_color)
        box['children'].append(colorbutton)

    def info(self, event):
        result = gui.infodialog(self, "Information!")
        print(repr(result))

    def warning(self, event):
        result = gui.warningdialog(self, "Warning!", title="Be warned!",
                                   buttons=["What's going to happen next?"])
        print(repr(result))

    def error(self, event):
        result = gui.errordialog(self, "Error!", title="Oh no!",
                                 buttons=["I'm screwed!", "I'm not screwed"])
        print(repr(result))

    def question(self, event):
        result = gui.questiondialog(self, "Do you like BananaGUI?",
                                    buttons=["Yes", "No"])
        print(repr(result))

    def choose_color(self, event):
        result = gui.colordialog(self, default=bananagui.RED,
                                 title="Choose a color")
        print(repr(result))


def main():
    with DialogTestWindow(title="Dialog test") as window:
        window['on_destroy'].append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
