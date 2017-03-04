from gi.repository import Gtk


def get_families():
    # Based on http://zetcode.com/gui/pygtk/pango/
    widget = Gtk.Label()
    context = widget.create_pango_context()
    return (family.get_name() for family in context.list_families())
