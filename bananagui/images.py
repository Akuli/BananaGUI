"""Classes for using images with BananaGUI."""

import os

import bananagui
from bananagui import utils


# Other imagetypes may be supported, but these are guaranteed to work.
_imagetypes = ('gif', 'png')


def _guess_imagetype(path, default):
    """Type-check the arguments and extract the imagetype from filename.

    >>> _guess_imagetype('a/b/c/coolpic.PNg', None)
    'png'
    >>> _guess_imagetype('whatever', 'Png')
    'png'
    >>> _guess_imagetype('whatever', None)
    Traceback (most recent call last):
      ...
    ValueError: cannot guess imagetype from 'whatever'
    """
    if not isinstance(path, str):
        raise TypeError("path should be a string, not %r" % (path,))
    if not (default is None or isinstance(default, str)):
        raise TypeError("imagetypes should be strings, not %r" % (path,))
    if default is None:
        filename = os.path.basename(path)
        if '.' not in filename:
            raise ValueError("cannot guess imagetype from %r" % path)
        return filename.rsplit('.', 1)[1].lower()
    return default.lower()


# TODO: resize() and flip() methods.
# TODO: methods for accessing pixels one by one?
class Image:
    __doc__ = """A mutable image.

    The imagetype is a string that is typically also the file the file
    extension without a dot. It's guessed from the filename if it's
    None. Not all imagetypes work with all GUI toolkits, but support
    for %s and %s images is guaranteed.

    The widgets.ImageLabel can be used for displaying an image to the
    user.
    """ % (', '.join(_imagetypes[:-1]), _imagetypes[-1])

    def __init__(self, path, imagetype=None):
        """Load an Image from a file.

        See the class documentation for more information about filetypes.
        """
        imagetype = _guess_imagetype(path, imagetype)
        wrapperclass = bananagui._get_wrapper('images:Image')
        self._wrapper, self._size = wrapperclass.from_file(path, imagetype)
        self._path = path

    @classmethod
    def from_size(cls, width, height):
        """Create a new, fully transparent Image from width and height."""
        for value in (width, height):
            if not isinstance(value, int):
                raise TypeError("expected an integer, got %r" % (value,))
            if value < 0:
                raise ValueError("%r is negative" % (value,))
        wrapperclass = bananagui._get_wrapper('images:Image')
        self = cls.__new__(cls)     # Don't run __init__.
        self._wrapper = wrapperclass.from_size(width, height)
        self._size = (width, height)
        self._path = None
        return self

    def __repr__(self):
        # Adding both path and size would make the repr awfully long,
        # but adding one of them seems good.
        cls = type(self)
        result = "%s.%s object" % (cls.__module__, cls.__name__)
        if self._path is None:
            result += ", size=%r" % (self.size,)
        else:
            result += " from %r" % self._path
        return '<' + result + '>'

    @property
    def real_image(self):
        """The real GUI toolkit's image object."""
        return self._wrapper.real_image

    @property
    def size(self):
        """Two-tuple of width and height as integers."""
        return self._size

    def copy(self):
        """Return a copy of this image.

        This image and the copy don't affect each other in any way when
        mutated.
        """
        cls = type(self)
        copy = cls.__new__(cls)     # Don't run __init__.
        copy._wrapper = self._wrapper.copy()
        copy._size = self._size
        copy._path = self._path
        return copy

    def save(self, path, imagetype=None):
        """Save the image to a file.

        See the class documentation for more information about filetypes.
        """
        imagetype = _guess_imagetype(path, imagetype)
        self._wrapper.save(path, imagetype)
        self._path = path
