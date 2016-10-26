from bananagui import gui


def main():
    template = ("This is line {} and it's pretty long because it "
                "contains a lot of text.")

    with gui.Window() as window:
        # This is one of the rare cases when new-style formatting is
        # actually useful.
        the_text = '\n'.join(map(template.format, range(20)))

        scrollarea = gui.ScrollArea(window)
        scrollarea['child'] = gui.Label(scrollarea, text=the_text)
        window['child'] = scrollarea

        window['on_destroy'].append(gui.quit)
        gui.main()


if __name__ == '__main__':
    main()
