class Widget:
    # TODO: implement background colors elsewhere also?

    # def __init__(self, **kwargs):
    #    # I have no idea why GTK+ makes changing the background color in
    #    # a non-deprecated (not-removed) way such a pain.
    #    self.__css = {}
    #    self.__provider = Gtk.CssProvider()
    #    context = self['base'].get_style_context()
    #    context.add_provider(self.__provider,
    #                         Gtk.STYLE_PROVIDER_PRIORITY_USER)
    #    super().__init__(**kwargs)
    #
    # def __update_css(self):
    #    words = []
    #    for item in self.__css.items():
    #        words.append('%s: %s;' % item)
    #    css = '* { %s }' % ' '.join(words)
    #    self.__provider.load_from_data(css.encode('utf-8'))
    #
    # def _bananagui_set_background(self, color):
    #    if color is None:
    #        try:
    #            del self.__css['background-color']
    #        except KeyError:
    #            pass
    #    else:
    #        self.__css['background-color'] = color.rgbstring
    #    self.__update_css()

    def __init__(self, bananawidget):
        self.bananawidget = bananawidget

    def focus(self):
        self.widget.grab_focus()


class Child(Widget):

    def set_expand(self, expand):
        h, v = expand
        self.widget.set_hexpand(h)
        self.widget.set_vexpand(v)

    def set_tooltip(self, tooltip):
        self.widget.set_tooltip_text(tooltip)

    def set_grayed_out(self, grayed_out):
        self.widget.set_sensitive(not grayed_out)
