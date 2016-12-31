# BananaGUI :banana:

This is a wrapper around the Python Tkinter and GTK+ 3 bindings. You can
write code using BananaGUI, and then run the same code using any of
these toolkits. BananaGUI may feature PyQt5 support later.

## Hello World!

A minimal Hello World program in BananaGUI looks like this:

```py
import bananagui
from bananagui import mainloop, widgets

bananagui.load('.tkinter')  # if you have it installed, try '.gtk3' also :)
with widgets.Window("Hello World") as window:
    window.add(widgets.Label("Hello World!"))
    window.on_close.connect(mainloop.quit)
    mainloop.run()
```

You can also write your GUI using the .ini format and then load it with
`bananagui.iniloader`:

```py
import bananagui
from bananagui import iniloader, mainloop


# Usually this would be in another file.
INI = """\
from bananagui import widgets

[window]
class = widgets.Window
title = "Hello World 3"

[label in window]
class = widgets.Label
text = "Hello World!"
"""


def main():
    bananagui.load('.tkinter')
    widgetdict = iniloader.load_ini(INI)
    # Now widgetdict is a dictionary.
    with widgetdict['window'] as window:
        window.on_close.connect(mainloop.quit)
        mainloop.run()

if __name__ == '__main__':
    main()
```

See [the guitests directory](guitests) for more examples.

## Why BananaGUI?

### The main reason

Many Python beginners have had a conversation like this:

    <beginner>      I want to make a simple GUI program with Python.
                    Which GUI toolkit should I use?
    <qtfan>         Use PyQt, it's cross-platform.
    <windowsuser>   I hate PyQt. It's a huge library with more than
                    enough features, installing the Windows version is
                    a real pain and their licensing solution sucks. Use
                    tkinter, it comes with Python so you don't need to
                    install anything.
    <linuxuser>     Tkinter looks like crap on my GTK+ based desktop,
                    and it doesn't come preinstalled on my system. Use
                    GTK+, it comes with my system and looks great.
    <windowsuser>   But installing GTK+ on Windows is even worse than
                    installing PyQt! It also looks awful on Windows.

As you can see, choosing the right GUI toolkit is not easy. Each
toolkit has its pros and cons, and none of them satisfies everyone's
needs. In the worst possible case, people choose one toolkit and later
rewrite the program using another toolkit. I have done this several
times.

This is when BananaGUI comes in. It allows you to write your
application once, and then run it with tkinter or GTK+ 3. Future
versions of BananaGUI will probably provide Qt support also. BananaGUI
isn't meant to replace any of these existing toolkits, it just provides
a high-level way to use them.

### Built-in documentation

PyQt and GTK+ Python bindings don't provide good documentation
strings for `help()`. For example, let's say that we want to know
something about checkboxes. This example uses GTK+, but PyQt works
similarly.

```
>>> from gi.repository import Gtk
>>> help(Gtk.CheckButton)
Help on class CheckButton in module gi.repository.Gtk:

class CheckButton(ToggleButton)
 |  :Constructors:
 |
 |  ::
 |
 |      CheckButton(**properties)
 |      new()
 |      new_with_label(label:str)
 |      new_with_mnemonic(label:str)
 |
 |  Method resolution order:
 |      CheckButton
 |      ToggleButton
 |      gi.overrides.Gtk.Button
 |      Button
 |      Bin
 |      gi.overrides.Gtk.Container
 |      Container
 |      gi.overrides.Gtk.Widget
 |      Widget
 |      gi.repository.GObject.InitiallyUnowned
 |      gi.overrides.GObject.Object
 |      gi.repository.GObject.Object
 |      gi._gobject._gobject.GObject
 |      gi.repository.Atk.ImplementorIface
 |      Buildable
 |      Actionable
 |      Activatable
 |      gobject.GInterface
 |      builtins.object
 |
 |  Data descriptors defined here:
 |
 |  toggle_button
 |
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |
 |  __gsignals__ = {}
 |
 |  __gtype__ = <GType GtkCheckButton (30187408)>
 |
 |  __info__ = ObjectInfo(CheckButton)
 |
 |  do_draw_indicator = gi.VFuncInfo(draw_indicator)
 |      draw_indicator(self, cr:cairo.Context)
 |
 |  new = gi.FunctionInfo(new)
 |      new()
 |
 |  new_with_label = gi.FunctionInfo(new_with_label)
 |      new_with_label(label:str)
 |
 |  new_with_mnemonic = gi.FunctionInfo(new_with_mnemonic)
 |      new_with_mnemonic(label:str)
 |
...
```

We have the names of all methods and information about the arguments
they take, but that's about it. There are no descriptions about what
the methods actually do. Instead, there are many implementation details
that we are not interested in and a ton of methods that we don't use
99% of the time. Tkinter is a little bit better when it comes to this,
but it's not perfect either.

I try my best to add docstrings everywhere in BananaGUI to make
`help()` as informative as possible. Here's the same thing in
BananaGUI:

```
>>> from bananagui import widgets
>>> help(widgets.Checkbox)
Help on class Checkbox in module bananagui.widgets:

class Checkbox(Child)
 |  A widget that can be checked.
 |
 |      ,-------------------.
 |      |   |   Check me!   |
 |      `-------------------'
 |
 |      ,-------------------.
 |      | X |  Uncheck me!  |
 |      `-------------------'
 |
 |  The Checkbox widget has nothing to do with the Box widget.
 |
 |  Attributes:
 |    text                  The text next to the checkbox.
 |    checked               True if the checkbox is checked currently.
 |                          False by default.
 |    on_checked_changed    A callback that runs on (un)check.
 |
 |  Method resolution order:
 |      Checkbox
 |      Child
 |      Widget
 |      bananagui.types.BananaObject
 |      builtins.object
 |
 |  Methods defined here:
 |
 |  __init__(self, text='', *, checked=False, **kwargs)
...
```

I think this is a lot better. We can get a good idea of what the
Checkbox is and how it works with just `help()`. There are no useless
implementation details showing up, and we even have ascii art pictures
of the widget.

BananaGUI doesn't implement the methods that we don't usually need, but
it exposes the real GUI toolkit widget it uses internally and it can be
accessed like `some_bananagui_widget.real_widget`.

### Debugging

When writing BananaGUI, I try to create informative error messages and
representations to make debugging easier. For example, let's create a
checkbox with tkinter and then have a look at it on the interactive
`>>>` prompt. This problem isn't tkinter-specific, GTK+ and PyQt5 also
have this.

```py
>>> import tkinter as tk
>>> root = tk.Tk()
>>> checkbox = tk.Checkbutton(root, text="Check me!")
>>> checkbox
<tkinter.Checkbutton object at 0x7f38ac29dd30>
>>>
```

So we know that it's a `tkinter.Checkbutton` and we know its memory
address. But if we have multiple checkboxes, that isn't really useful
for distinguishing them from each other.

Let's do the same thing with BananaGUI:

```py
>>> from bananagui import load, widgets
>>> load('.tkinter')
>>> checkbox = widgets.Checkbox("Check me!")
>>> checkbox
<bananagui.widgets.Checkbox object, text='Check me!', checked=False>
```

I think this is a lot better. The `__repr__` method returned a good
description of the widget. It's brief, but a lot more helpful than a
memory address.

## Developing BananaGUI

### Where is everything?

BananaGUI consists of the public API and the `bananagui.wrappers`
submodule. The wrappers submodule contains a bunch of modules that each
"wrap" a GUI toolkit and provide a way to use it. The `bananagui.load()`
function simply imports one of these wrapper modules and sets it to
`bananagui._wrapper`, and rest of BananaGUI finds it there. Most of the
public API uses `bananagui._get_wrapper()` to access the currently
loaded wrapper.

### Tests

BananaGUI uses three kinds of tests:
- Unit tests in [the tests directory](tests/).
- Doctests in files.
- [GUI tests](guitests/) are small programs written using BananaGUI.

The BananaGUI wrappers are meant to be tested entirely with GUI tests
because it's an easy way to make sure that everything works.

    $ yourpython -m guitests some_wrapper

Of course, replace `yourpython` with a working Python program and
`some_wrapper` with a valid argument to `bananagui.load()`. See
`help('bananagui.load')`.

You need to [install pytest](https://pytest.readthedocs.io/en/latest/getting-started.html#installation)
to run the unit tests and doctests:

    $ yourpython -m pytest

If you're interested in the coverage you can [install
coverage.py](https://coverage.readthedocs.io/en/coverage-4.3.1/install.html#install)
and run pytest with it:

    $ yourpython -m coverage run -m pytest
    $ yourpython -m coverage report --include='bananagui/*'

Or you can generate a nice HTML report:

    $ yourpython -m coverage html --include='bananagui/*'
    $ yourpython -m webbrowser htmlcov/index.html

Keep in mind that the coverage of `bananagui.widgets` looks worse than
it really is because a lot of the testing is taken care of by the
guitests.

## Thanks

I want to thank these people for helping me write BananaGUI:

- [The 8Banana Organization](https://github.com/8Banana)
