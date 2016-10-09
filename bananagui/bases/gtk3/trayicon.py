import os
import warnings

from gi.repository import Gtk

from . import has_appindicator
if has_appindicator:
    from gi.repository import AppIndicator3  # noqa
else:
    # Make the linter happy :)
    AppIndicator3 = None


class TrayIcon:

    def __init__(self, iconpath):
        if has_appindicator:
            widget = AppIndicator3.Indicator.new(
                # Unfortunately there's no good way to get the name of
                # the application.
                'bananagui-application',
                # AppIndicator3 thinks this is an icon name if this is
                # not an absolute path.
                os.path.abspath(iconpath),
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
            )
            widget.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            # We need to set a menu to make the indicator display itself.
            widget.set_menu(Gtk.Menu())
        else:
            # Fall back to deprecated Gtk.StatusIcon.
            widget = Gtk.StatusIcon()
            widget.set_from_file(iconpath)
        self.real_widget.raw_set(widget)
        super().__init__()

    def _bananagui_set_tooltip(self, tooltip):
        if has_appindicator:
            # Unfortunately AppIndicator3 doesn't support tooltips.
            warnings.warn("AppIndicator3 doesn't support tooltips")
        else:
            self['real_widget'].set_tooltip_text(tooltip)
