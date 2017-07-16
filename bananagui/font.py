import functools

from bananagui import mainloop, _modules
from bananagui._types import UpdatingProperty, UpdatingObject, get_class_name


# widgets should have properties that can be set to Font objects, but if
# it hasn't been set, creates a new Font object when requested
# TODO: tkinter's font sizes can be negative, handle them somehow
class Font(UpdatingObject):
    """A class that represents a font.

    :mod:`bananagui.mainloop` needs to be initialized before creating
    Font objects.

    Usually it's a bad idea to do this::

        font = bananagui.Font('DejaVu Sans', 12)

    The problem here is that many systems don't have a "DejaVu Sans"
    font installed, and not all users like their font exactly 12 pixels
    high. Future versions of BananaGUI may feature some kind of font
    dialog that lets users select fonts, but currently that's not
    implemented. If you're really desperate you can make a font dialog
    yourself with :meth:`Font.list_families`, a size :class:`.Spinbox`
    and 3 :class:`Checkbox` widgets for :attr:`bold`, :attr:`italic` and
    :attr:`underline`.

    However, there's nothing wrong with doing something relative to the
    fonts. For example, you can make the font bigger like this::

        some_widget.font.size *= 2
    """

    family = UpdatingProperty.with_attr('_family')
    size = UpdatingProperty.with_attr('_size')
    bold = UpdatingProperty.with_attr('_bold')
    italic = UpdatingProperty.with_attr('_italic')
    underline = UpdatingProperty.with_attr('_underline')

    def __init__(self, family, size, *, bold=False, italic=False,
                 underline=False):#, overline=False):
        mainloop._check_initialized()
        self._family = family
        self._size = size
        self._bold = bold
        self._italic = italic
        self._underline = underline

        if _modules.name == 'tkinter':
            self.real_font = _modules.font.Font()
            self._monospace_family = None
        else:
            raise NotImplementedError
        self.update_state()

    def __repr__(self):
        parts = [repr(self.family), repr(self.size)]
        for attribute in ['bold', 'italic', 'underline']:#, 'overline']:
            value = getattr(self, attribute)
            if value:
                # the default is False, but this is True
                parts.append('%s=%r' % (attribute, value))
        return '%s(%s)' % (get_class_name(type(self)), ', '.join(parts))

    def update_state(self):
        if _modules.name == 'tkinter':
            if self.family.casefold() == 'monospace':
                tkfixed = _modules.font.Font(name='TkFixedFont', exists=True)
                self.real_font['family'] = tkfixed.actual('family')
            else:
                self.real_font['family'] = self.family
            self.real_font['size'] = self.size
            self.real_font['weight'] = 'bold' if self.bold else 'normal'
            self.real_font['slant'] = 'italic' if self.italic else 'roman'
            self.real_font['underline'] = self.underline
        else:
            raise NotImplementedError

    _family_cache = set()

    @staticmethod
    def list_families():
        """Get a list of all valid :attr:`family` values."""
        cache = Font._family_cache     # less typing ftw
        if not cache:
            cache.add('Monospace')
            if _modules.name == 'tkinter':
                # TODO: figure out why some families start with @ on
                # windows and maybe do something with them instead of
                # ignoring?
                cache.update(family for family in _modules.font.families()
                             if not family.startswith('@'))
            elif _modules.name.startswith('gtk'):
                # based on http://zetcode.com/gui/pygtk/pango/
                dummy_widget = _modules.Gtk.Label()
                context = dummy_widget.create_pango_context()
                cache.update(
                    family.get_name() for family in context.list_families())
            else:
                raise NotImplementedError

        # it's important to return a copy of the cache because someone
        # might mutate the returned list
        return sorted(cache, key=str.casefold)
