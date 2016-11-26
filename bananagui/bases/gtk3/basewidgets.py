# Copyright (c) 2016 Akuli

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from gi.repository import Gtk


class Widget:
    # TODO: implement background colors elsewhere also?

#    def __init__(self, **kwargs):
#        # I have no idea why GTK+ makes changing the background color in
#        # a non-deprecated (not-removed) way such a pain.
#        self.__css = {}
#        self.__provider = Gtk.CssProvider()
#        context = self['real_widget'].get_style_context()
#        context.add_provider(self.__provider,
#                             Gtk.STYLE_PROVIDER_PRIORITY_USER)
#        super().__init__(**kwargs)
#
#    def __update_css(self):
#        words = []
#        for item in self.__css.items():
#            words.append('%s: %s;' % item)
#        css = '* { %s }' % ' '.join(words)
#        self.__provider.load_from_data(css.encode('utf-8'))
#
#    def _bananagui_set_background(self, color):
#        if color is None:
#            try:
#                del self.__css['background-color']
#            except KeyError:
#                pass
#        else:
#            self.__css['background-color'] = color.rgbstring
#        self.__update_css()

    def _focus(self):
        self.real_widget.grab_focus()


class Parent:
    pass


class Child:

    def _set_expand(self, expand):
        h, v = expand
        self.real_widget.set_hexpand(h)
        self.real_widget.set_vexpand(v)

    def _set_tooltip(self, tooltip):
        self.real_widget.set_tooltip_text(tooltip)

    def _set_grayed_out(self, grayed_out):
        self.real_widget.set_sensitive(not grayed_out)
