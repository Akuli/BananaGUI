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

import os
import warnings

from gi.repository import Gtk

from . import HAS_APPINDICATOR

if HAS_APPINDICATOR:
    # Everything in this module starts with "Indicator" so I think it's
    # fine to use a from import.
    from gi.repository.AppIndicator3 import (
        Indicator, IndicatorCategory, IndicatorStatus)


class TrayIcon:

    def __init__(self, **kwargs):
        if HAS_APPINDICATOR:
            # This is a bit bad. There's no good way to get the name of
            # the application, and we also don't know the icon yet so
            # we need to set that to a dummy value.
            widget = Indicator.new(
                'bananagui-application',
                'dummy-icon-name',
                IndicatorCategory.APPLICATION_STATUS,
            )
            widget.set_status(IndicatorStatus.ACTIVE)
            # We need to set a menu to show the indicator.
            widget.set_menu(Gtk.Menu())
        else:
            # Fall back to deprecated Gtk.StatusIcon.
            widget = Gtk.StatusIcon()
        self.real_widget.raw_set(widget)
        super().__init__(**kwargs)

    def _bananagui_set_iconpath(self, path):
        if HAS_APPINDICATOR:
            # This needs to be absolute path or AppIndicator3 thinks
            # it's an icon name.
            self['real_widget'].set_icon(os.path.abspath(path))
        else:
            self['real_widget'].set_from_file(path)

    def _bananagui_set_tooltip(self, tooltip):
        if HAS_APPINDICATOR:
            warnings.warn("AppIndicator3 doesn't support tooltips",
                          RuntimeWarning)
        else:
            self['real_widget'].set_tooltip_text(tooltip)
