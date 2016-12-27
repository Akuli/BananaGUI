from bananagui import mainloop, widgets


def main():
    template = ("This is line {} and it's pretty long because it "
                "contains a lot of text.")

    with widgets.Window() as window:
        # This is one of the rare cases when new-style formatting is
        # actually useful.
        the_text = '\n'.join(map(template.format, range(20)))

        scroller = widgets.Scroller()
        scroller.child = widgets.Label(the_text)
        window.child = scroller
        print(scroller)

        window.on_close.append(mainloop.quit)
        mainloop.run()


if __name__ == '__main__':
    main()
