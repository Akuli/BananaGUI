from gi.repository import Gtk


class Widget:

    def __init__(self, **kwargs):
        widget = self['real_widget']

        # I have no idea why GTK+ makes changing the background color in
        # a non-deprecated (not-removed) way such a pain.
        self.__css = {}
        self.__provider = Gtk.CssProvider()
        context = self['real_widget'].get_style_context()
        context.add_provider(self.__provider,
                             Gtk.STYLE_PROVIDER_PRIORITY_USER)

        super().__init__(**kwargs)

    def __update_css(self):
        words = []
        for item in self.__css.items():
            words.append('%s: %s;' % item)
        css = '* { %s }' % ' '.join(words)
        self.__provider.load_from_data(css.encode('utf-8'))

    def _bananagui_set_tooltip(self, tooltip):
        self['real_widget'].set_tooltip_text(tooltip)

    def _bananagui_set_background(self, color):
        if color is None:
            try:
                del self.__css['background-color']
            except KeyError:
                pass
        else:
            self.__css['background-color'] = color.rgbstring
        self.__update_css()


class Parent:
    pass


class Child:

    def _bananagui_set_expand(self, expand):
        horizontal, vertical = expand
        self['real_widget'].set_hexpand(horizontal)
        self['real_widget'].set_vexpand(vertical)

    def _bananagui_set_grayed_out(self, grayed_out):
        self['real_widget'].set_sensitive(not grayed_out)


class Dummy:

    def __init__(self, parent, **kwargs):
        self.real_widget.raw_set(Gtk.Label())
        super().__init__(parent, **kwargs)
