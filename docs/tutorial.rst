Beginner-Friendly Tutorial
==========================

This is a beginner-friendly introduction to writing GUI programs with 
BananaGUI.

What is BananaGUI?
------------------

A Graphical User Interface or **GUI** is a way to use a program without
a terminal or a command prompt. Usually GUI's consist of one or more
windows and different kinds of things inside the windows. Most web
browsers, text editors, games and other programs have GUI's.

Usually GUI programs are written using a **GUI toolkit**. They take care
of displaying windows and different things inside the windows for the
programmer, and the programmer just needs to tell the GUI toolkit what
to do using a programming language like Python. Some of the most popular
GUI toolkits are tkinter, GTK+ and Qt.

A common problem is that programs written in different GUI toolkits look
different. For example, most programs meant for Linux users use GTK so
GTK programs look good native Linux. But GTK programs look a bit
different than other applications on Windows and OSX, so tkinter is a
better choice for Windows and OSX programs.

BananaGUI is not a GUI toolkit. It's not trying to compete with GUI
toolkits or replace them, it just provides an easy way to use them. You
can write a GUI program using BananaGUI and then run it using whatever
GUI toolkit you want. There's no need to install new GUI toolkits or
worry about what your program will look like on different platforms.

**TODO:** Installing instructions.

.. _tut-hello-world:

Hello World!
------------

Our first program will display a window like this:

.. code-block:: none

    ,---------------------.
    |  Hello  | _ | o | X |
    |---------------------|
    |                     |
    |                     |
    |                     |
    |     Hello World!    |
    |                     |
    |                     |
    |                     |
    `---------------------'

As you can see, I'm really lazy at taking screenshots so BananaGUI's 
documentation contains ASCII art instead.

Here's the code::

    import bananagui

    bananagui.init(['gtk3', 'tkinter'])

    window = bananagui.Window("Hello")
    label = bananagui.Label("Hello World!")
    window.add(label)

    window.on_close.connect(bananagui.quit)
    bananagui.run()

Let's go through the code and see how it works.

.. _tut-init:

Initializing BananaGUI
-----------------------

::
    bananagui.init(['gtk3', 'tkinter'])

We need to tell BananaGUI which GUI toolkit it should use. The
:func:`bananagui.init` function takes a GUI toolkit name as an argument
and loads it. We can also give it a list of wrapper names, so this line
of code attempts to load GTK and loads tkinter if GTK isn't installed.

Future versions of BananaGUI will probably support choosing the GUI
toolkit automatically based on the platform.

By the way, most function and class names like this
:func:`bananagui.init` thing are actually links. You can click them if
you want to read more about them.

.. _tut-widgets:

Widgets
-------

::
    window = bananagui.Window("Hello")
    label = bananagui.Label("Hello World!")
    window.add(label)

Like other GUI libraries, BananaGUI uses **widgets**. A widget is a part
of the GUI. For example, here we want to create a window with some text
in it, so we need a widget that represents the window and a widget that
shows the text. We'll using :class:`bananagui.Window` is a window widget, and
:class:`bananagui.Label` is a widget that displays text.

You can also use the ``>>>`` prompt to experiment with these things.
It's usually best to use BananaGUI without actually using a GUI toolkit
at all with ``bananagui.init('dummy')``. You won't actually see the
widgets, but you can still try things out and see how they behave::

    >>> import bananagui
    >>> bananagui.init('dummy')
    >>> window = bananagui.Window("Hello")
    >>> window
    <bananagui.Window widget, title='Hello', contains nothing>
    >>> label = bananagui.Label("Hello World!")
    >>> label
    <bananagui.Label widget, text='Hello World!'>
    >>> window.add(label)
    >>> window
    <bananagui.Window widget, title='Hello', contains a bananagui.Label>

It's also possible to do the same thing without ``'dummy'``, but the
widgets might not show up at all, the window may be unresponsive or you
may notice other problems. We'll learn more about this in `The Main Loop`_.

.. this contains non-ascii but the source code doesn't because pep 8 :(

If you have a big project with many widgets, it may be useful to print a 
tree of the widgets you have using :mod:`bananagui.widgettree`::

    >>> from bananagui import widgettree
    >>> widgettree.dump(window)
    <bananagui.Window widget, title='Hello', contains a bananagui.Label>
    ╰── <bananagui.Label widget, text='Hello World!'>

.. _tut-attributes:

Attributes
----------

When we created a window like ``window = bananagui.Window("Hello")``,
the ``"Hello"`` wasn't thrown away. You can still get that or change the
title of the window to whatever you want using ``window.title``::

    >>> window.title
    'Hello'
    >>> window.title = "New Title"
    >>> window.title
    'New title'
    >>> window
    <bananagui.Window widget, title='New Title', contains a bananagui.Label>

The text of the label works the same way::

    >>> label.text = "New text"
    >>> label
    <bananagui.Label widget, text='New text'>

Many things in BananaGUI work like this. You can give the value using an 
argument when you create the widget, or you can use an attribute to 
change it later.

.. _tut-mainloop:

The main loop
-------------

::
    bananagui.run()

Now our hello world program has a window object, but the window might
not be actually visible yet. Some GUI toolkits display windows right
away while others don't.

After setting everything up, we need to call :func:`bananagui.run` and
wait for something to stop it. When it's running, we can be sure that
the user sees the widgets we created.

Usually everything before :func:`bananagui.run` takes just a
fraction of a second to run, but the mainloop is running all the time
when the program is used. It might be anything from a couple seconds to
several hours.

.. _tut-callbacks:

Callbacks
---------

::
    window.on_close.connect(bananagui.quit)

Try removing this line from the hello world program and running it. If
you try to close the window, nothing happens and the program just keeps
running! Most wrappers should allow interrupting the program normally by
pressing Ctrl+C.

You can stop the main loop at any time by calling
:func:`bananagui.quit`. Now we just need to tell BananaGUI to
run it when the user tries to close the window.

BananaGUI has **callbacks** for things like this. A callback can be
connected to a function, and then that function will be called when the
user does something. For example, :data:`bananagui.Window.on_close` is a
BananaGUI callback. Let's try it out::

    >>> import bananagui
    >>> bananagui.init('dummy')
    >>> window = bananagui.Window()
    >>> window.on_close
    bananagui.Callback()
    >>> def callback_func():
    ...     print("running the callback function")
    ... 
    >>> window.on_close.connect(callback_func)
    >>> window.on_close.run()
    running the callback function

.. note::
    The correct syntax is ``callback.connect(function)``, not
    ``callback.connect(function())``. Doing ``function()`` always runs
    the function right away, but we want to run the callback later.

You can connect multiple functions to one callback, and they will all be
called when the callback runs::

    >>> def another_callback():
    ...     print("now the second callback function runs too")
    ... 
    >>> window.on_close.connect(another_callback)
    >>> window.on_close.run()
    running the callback function
    now the second callback function runs too

.. seealso:: `Passing Arguments to Callback Functions`_

.. _tut-bins:

Bins
----

What if we want to add two labels into one window? Try that out on the 
``>>>`` prompt, and you'll notice that the window doesn't like that at 
all::

    >>> window.add(bananagui.Label("Test 1"))
    >>> window.add(bananagui.Label("Test 2"))
    Traceback (most recent call last):
      ...
    ValueError: there's already a child widget, remove it before adding another widget

:class:`bananagui.Bin` widgets can have one child or no children at all,
and BananaGUI windows are Bin widgets. This may feel stupid right now,
but BananaGUI would be more complicated without widgets like this. See
`Boxes`_ if you want to add more than one widget to a window.

You can get the child of a Bin widget after adding it with the ``child``
attribute::

    >>> window.child
    <bananagui.Label widget, text='Test 1'>

Or you can get rid of the child using the ``remove`` method::

    >>> window
    <bananagui.Window widget, title='BananaGUI Window', contains a bananagui.Label>
    >>> window.remove(window.child)
    >>> window
    <bananagui.Window widget, title='BananaGUI Window', contains nothing>
    >>> window.child is None
    True
    >>> 
