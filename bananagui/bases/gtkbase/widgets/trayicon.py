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

from . import GOT_APPINDICATOR

if GOT_APPINDICATOR:
    # Everything in this module starts with "Indicator" so I think it's
    # fine to use a from import.
    from gi.repository.AppIndicator3 import (
        Indicator, IndicatorCategory, IndicatorStatus)


class TrayIcon:

    def __init__(self, **kwargs):
        if GOT_APPINDICATOR:
            # This is a bit bad. There's no good way to get the name of
            # the application, and we also need to set the icon to a
            # dummy value if we don't have that.
            self.base = Indicator.new(
                'bananagui-application',
                kwargs.get('iconpath', 'dummy-icon-name'),
                IndicatorCategory.APPLICATION_STATUS,
            )
            self.base.set_status(IndicatorStatus.ACTIVE)
            # We need to set a menu to show the indicator.
            self.base.set_menu(Gtk.Menu())
        else:
            # Fall back to deprecated Gtk.StatusIcon.
            self.base = Gtk.StatusIcon()
        super().__init__(**kwargs)

    def _set_iconpath(self, path):
        if GOT_APPINDICATOR:
            # This needs to be absolute path or AppIndicator3 thinks
            # it's an icon name.
            self.base.set_icon(os.path.abspath(path))
        else:
            self.base.set_from_file(path)

    def _set_tooltip(self, tooltip):
        if GOT_APPINDICATOR:
            warnings.warn("AppIndicator3 doesn't support tooltips",
                          RuntimeWarning)
        else:
            self.base.set_tooltip_text(tooltip)
