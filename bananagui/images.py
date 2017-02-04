# Copyright (c) 2016-2017 Akuli

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

"""Classes for using images with BananaGUI."""

import os

from bananagui import _get_wrapper

__all__ = ['Image']


def _guess_filetype(path, default):
    """Extract the filetype from filename.

    >>> _guess_filetype('a/b/c/coolpic.PNg', None)
    'png'
    >>> _guess_filetype('whatever', 'Png')
    'png'
    >>> _guess_filetype('whatever', None)
    Traceback (most recent call last):
      ...
    ValueError: cannot guess filetype from 'whatever'
    """
    if default is None:
        filename = os.path.basename(path)
        if '.' not in filename:
            raise ValueError("cannot guess filetype from %r" % path)
        return filename.rsplit('.', 1)[1].lower()
    return default.lower()


# TODO: resize() and flip() methods.
# TODO: methods for accessing pixels one by one?
class Image:
    """A mutable image.

    Calling the Image class constructs a new image from a path to a 
    file. For example, ``Image('banana.png')`` creates a new image of 
    the file ``banana.png`` in the current working directory.

    The filetype is typically also the file the file extension without a 
    dot. Not all filetypes work with all GUI toolkits, but ``'gif'`` and 
    ``'png'`` should be valid filetype values with all GUI toolkits. The 
    filetype must be given explicitly if it can't be guessed from the 
    file extension, like ``Image('magic-banana', 'gif')``.

    You can use :class:`bananagui.widgets.ImageLabel` for displaying an 
    image to the user.
    """

    def __init__(self, path: str, filetype: str = None):
        """Load an Image from a file."""
        filetype = _guess_filetype(path, filetype)
        wrapperclass = _get_wrapper('images:Image')
        self._wrapper, self._size = wrapperclass.from_file(path, filetype)
        self._path = path

    def save(self, path: str, filetype: str = None):
        """Save the image to a file."""
        filetype = _guess_filetype(path, filetype)
        self._wrapper.save(path, filetype)
        self._path = path

    @classmethod
    def from_size(cls, width: int, height: int):
        """Create a new, fully transparent Image of the given size."""
        if width < 0 or height < 0:
            raise ValueError("negative width or height")
        wrapperclass = _get_wrapper('images:Image')
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
        """Two-tuple of width and height in pixels."""
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
