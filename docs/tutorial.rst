Beginner-friendly tutorial
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

On the other hand, BananaGUI is not a GUI toolkit. It's not trying to 
compete with GUI toolkits or replace them, it just provides an easy way 
to use them. You can write a GUI program using BananaGUI and then run it 
using whatever GUI toolkit you want. In other words, BananaGUI is
**a wrapper** around GUI toolkits.

**TODO:** Installing instructions.

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

Importing and loading BananaGUI
-------------------------------

The first thing we need to do is to import everything we need from 
BananaGUI.

.. code-block:: python

   from bananagui import load_wrapper, mainloop, widgets

Next we need to load a wrapper that wraps a GUI toolkit. The 
:func:`bananagui.load_wrapper` function takes a wrapper name as an 
argument and loads that wrapper. We can also give it more than one name, 
and BananaGUI will try to load the first wrapper, and if it fails it 
will try the next one and so on.

.. code-block:: python

   load_wrapper('tkinter', 'gtk3')

If you are using Windows or OSX and you installed your Python yourself, 
BananaGUI will probably use tkinter as its GUI toolkit. If you're using 
Linux you probably don't have tkinter installed but you might have GTK+, 
so BananaGUI will use that.

Sometimes it's handy to play around with BananaGUI without actually 
using a real GUI toolkit at all. There's a special wrapper called 
``dummy`` just for that, and we'll use it later in this tutorial.

Now we are ready to create the window!

Widgets
-------

Like other GUI libraries, BananaGUI uses **widgets**. A widget is a part 
of the GUI. For example, if we have a window with a button in it, we 
have two widgets. The window is a widget, and the button is a widget.

The :mod:`bananagui.widgets` module contains BananaGUI's widget classes. 
Our example program will display a window with the title "Hello" and 
some text inside it. So we need two widgets, the window and something to 
display the text.

:class:`bananagui.widgets.Window` is used for creating windows, and 
:class:`bananagui.widgets.Label` is a widget that displays text. We can 
create a window and add a label into it like this:

.. code-block:: python

   window = widgets.Window("Hello")
   label = widgets.Label("Hello World!")
   window.add(label)

You can also use the ``>>>`` prompt and the dummy wrapper to experiment 
with these things.

.. code-block:: python

   >>> from bananagui import load_wrapper, widgets
   >>> load_wrapper('dummy')
   >>> window = widgets.Window("Hello")
   >>> window
   <bananagui.widgets.Window object, title='Hello', empty>
   >>> label = widgets.Label("Hello World!")
   >>> label
   <bananagui.widgets.Label object, text='Hello World!'>
   >>> window.add(label)
   >>> window
   <bananagui.widgets.Window object, title='Hello', contains a child>

It's also possible to use other wrappers than ``dummy`` with the ``>>>`` 
prompt, but the window might not show up at all, it may be unresponsive 
or you may notice other problems. We'll learn more about this in
`The main loop`_.

If you have a big project with many widgets, it may be useful to print a 
tree of the widgets you have using :mod:`bananagui.widgettree`:

.. code-block:: python

   >>> from bananagui import widgettree
   >>> widgettree.dump(window)
   bananagui.widgets.Window object, title='Hello', contains a child
   └── bananagui.widgets.Label object, text='Hello World!'

Attributes
----------

When we created a window like ``window = widgets.Window("Hello")``, the 
``"Hello"`` wasn't thrown away. You can still get that or change the 
title of the window to whatever you want using ``window.title``.

.. code-block:: python

   >>> window.title
   'Hello'
   >>> window.title = "New title"
   >>> window.title
   'New title'
   >>> window
   <bananagui.widgets.Window object, title='New title', empty>

The text of the label works the same way:

.. code-block:: python

   >>> label.text = 'New text'
   >>> label
   <bananagui.widgets.Label object, text='New text'>

Many things in BananaGUI work like this. You can give the value using an 
argument when you create the widget, or you can use an attribute to 
change it later.

The main loop
-------------

Now our hello world program has a window object, but the window might 
not be actually visible yet. Some GUI toolkits display windows right 
away, some don't.

BananaGUI uses the GUI toolkit's main event loop, and you can control it 
with the :mod:`bananagui.mainloop` module. It's easy to use: after 
setting everything up, we call :func:`bananagui.mainloop.run` and wait 
for something to stop it. When it's running, we can be sure that the 
user sees the widgets we created.

.. code-block:: python

   mainloop.run()

This function is typically running for a long time. Usually everything 
before this takes just a fraction of a second, but the mainloop is 
running all the time when the program is used. It might be anything from 
a couple seconds to several hours.

So now our code looks like this:

.. code-block:: python

   from bananagui import load_wrapper, mainloop, widgets
   
   load_wrapper('tkinter', 'gtk3')
   
   window = widgets.Window("Hello")
   label = widgets.Label("Hello World!")
   window.add(label)
   mainloop.run()

Run this program. If everything works, then that's awesome! You have 
created your first BananaGUI application.

Callbacks
---------

Our hello world program has a problem. If you try to close the window, 
the program just keeps running! Most wrappers should allow interrupting 
the program normally by pressing Ctrl+C.

So we need to improve the program to stop the mainloop when the user 
closes the window. There's a :func:`bananagui.mainloop.quit` function 
for stopping :func:`bananagui.mainloop.run`, but how can we call that 
when the window is closed?

BananaGUI has **callbacks** for things like this. A callback can be 
connected to a function, and then that function will be called when the 
user does something.

Our window has a callback called ``on_close``, and it runs when the user 
closes the window. Let's try it out on the ``>>>`` prompt.

.. code-block:: python

   >>> from bananagui import load_wrapper, widgets
   >>> load_wrapper('dummy')
   >>> window = widgets.Window()
   >>> window.on_close
   <BananaGUI callback 'on_close' of bananagui.widgets.Window object>
   >>> def callback_func():
   ...     print("running the callback function")
   ...
   >>> window.on_close.connect(callback_func)
   >>> window.on_close.run()
   running the callback function

Usually you don't need to use the ``run()`` method yourself, BananaGUI 
calls it when the user does something and runs your callbacks. So let's 
solve the window closing problem.

.. code-block:: python

   window.on_close.connect(mainloop.quit)

Now our code looks like this:

.. code-block:: python

   from bananagui import load_wrapper, mainloop, widgets
   
   load_wrapper('tkinter', 'gtk3')
   
   window = widgets.Window("Hello")
   label = widgets.Label("Hello World!")
   window.add(label)
   window.on_close.connect(mainloop.quit)
   mainloop.run()

.. seealso:: `Passing arguments to callback functions`_.

Bins
----

What if we want to add two labels into one window? Try that out on the 
``>>>`` prompt, and you'll notice that the window doesn't like that at 
all.

.. code-block:: python

   >>> window = widgets.Window("Test")
   >>> window.add(widgets.Label("Test 1"))
   >>> window.add(widgets.Label("Test 2"))
   Traceback (most recent call last):
     ...
   ValueError: there's already a child, cannot add()

This is because BananaGUI windows are instances of 
:class:`bananagui.widgets.Bin`. Bin widgets can have one child or no 
children at all. This may feel stupid right now, but BananaGUI would be 
more complicated without widgets like this.

You can get the child of a Bin widget after adding it using the 
``child`` attribute.

.. code-block:: python

   >>> window.child
   <bananagui.widgets.Label object, text='Test 1'>

Or you can get rid of the child using the ``remove`` method:

.. code-block:: python

   >>> window
   <bananagui.widgets.Window object, title='BananaGUI Window', contains a child>
   >>> window.remove(window.child)
   >>> window
   <bananagui.widgets.Window object, title='BananaGUI Window', empty>

Boxes
-----

The window can have only one child, but it doesn't mean that there's no 
way to have two labels in it. The easiest way to do that is to create a 
:class:`bananagui.widgets.Box`, and then add the labels into the box. 
Let's make a program that creates a window like this:

.. code-block:: none

   ,------------------------.
   |  Box test  | _ | o | X |
   |------------------------|
   |                        |
   |         Label 1        |
   |                        |
   | - - - - - - - - - - - -|
   |                        |
   |         Label 2        |
   |                        |
   `------------------------'

Here's the program.

.. code-block:: python

   from bananagui import load_wrapper, mainloop, widgets
   
   load_wrapper('tkinter', 'gtk3')
   
   window = widgets.Window("Box test")
   box = widgets.Box()
   box.append(widgets.Label("Label 1"))
   box.append(widgets.Label("Label 2"))
   window.add(box)
   
   window.on_close.connect(mainloop.quit)
   mainloop.run()

If you run the program you'll notice that it displays two labels above 
each other, just like we wanted it to do.

Let's print a tree of it:

.. code-block:: python

   >>> window = widgets.Window("Box test")
   >>> box = widgets.Box()
   >>> box.append(widgets.Label("Label 1"))
   >>> box.append(widgets.Label("Label 2"))
   >>> window.add(box)
   >>> widgettree.dump(window)
   bananagui.widgets.Window object, title='Box test', contains a child
   └── bananagui.widgets.Box object, contains 2 children
       ├── bananagui.widgets.Label object, text='Label 1'
       └── bananagui.widgets.Label object, text='Label 2'

You might be wondering why we add a child widget to the window using a 
method called ``add``, but boxes have an ``append`` method instead. 
Lists also have a method called ``append``, and this is not just a 
random coincidence. Boxes actually behave like lists in many ways:

.. code-block:: python

   >>> box[0]
   <bananagui.widgets.Label object, text='Label 1'>
   >>> box[1]
   <bananagui.widgets.Label object, text='Label 2'>
   >>> box[:]
   [<bananagui.widgets.Label object, text='Label 1'>,
    <bananagui.widgets.Label object, text='Label 2'>]
   >>> box[::-1]
   [<bananagui.widgets.Label object, text='Label 2'>,
    <bananagui.widgets.Label object, text='Label 1'>]

Boxes also have most of the methods that list have. So if you can do 
something to a list, you should be able to do the same thing to a box.

It's also possible to add widgets next to each other:

.. code-block:: none

   ,---------------------------.
   |  Box test 2   | _ | o | X |
   |---------------------------|
   |             |             |
   |   Label 1   |   Label 2   |
   |             |             |
   `---------------------------'

All we need to do is to make the box horizontal using the *HORIZONTAL* 
member of :class:`bananagui.Orient`. The boxes are vertical by default 
because most of the time we use vertical boxes more than horizontal 
boxes.

.. code-block:: python

   from bananagui import Orient, load_wrapper, mainloop, widgets
   
   load_wrapper('tkinter', 'gtk3')
   
   window = widgets.Window("Test")
   box = widgets.Box(Orient.HORIZONTAL)
   box.append(widgets.Label("Label 1"))
   box.append(widgets.Label("Label 2"))
   window.add(box)
   
   window.on_close.connect(mainloop.quit)
   mainloop.run()

Buttons
-------

So far our program displays some text and that's it. Really boring! We 
want to have a button that does something when we click it.

Creating a button is easy. Just create a 
:class:`bananagui.widgets.Button` like ``widgets.Button("some text")``.

.. code-block:: python

   >>> button = widgets.Button("Click me!")
   >>> button
   <bananagui.widgets.Button object, text='Click me!'>

Button widgets have an ``on_click`` callback, just like the ``on_close`` 
callback that windows have. It's ran when the button is clicked, and it 
does nothing by default. See `Callbacks`_ for more information about 
them.

.. code-block:: python

   >>> button.on_click
   <BananaGUI callback 'on_click' of bananagui.widgets.Button object>

So here's a program that prints hello when the user clicks the button:

.. code-block:: python

   from bananagui import load_wrapper, mainloop, widgets
   
   load_wrapper('tkinter', 'gtk3')
   
   def print_hello():
       print("Hello!")
   
   window = widgets.Window("Test")
   box = widgets.Box()
   window.add(box)
   
   label = widgets.Label("This is a test.")
   box.append(label)
   button = widgets.Button("Print hello")
   button.on_click.connect(print_hello)
   box.append(button)
   
   window.on_close.connect(mainloop.quit)
   mainloop.run()

The program runs like this:

.. code-block:: none

   ,-------------------------------------------.
   |  Command prompt or terminal   | _ | o | X |
   |-------------------------------------------|
   | $ python3 buttontest.py                   |
   | Hello!                                    |
   | Hello!        ,-------------------------------.
   | Hello!        |  Button test      | _ | o | X |
   |               |-------------------------------|
   |               |                               |
   |               |        This is a test.        |
   |               |                               |
   |               | ,---------------------------. |
   |               | |                           | |
   |               | |        Print hello        | |
   |               | |              |\           | |
   |               | `--------------|_\----------' |
   |               `-----------------|\------------'
   |                                           |
   `-------------------------------------------'

The terminal, command prompt or whatever you're running the program from 
displays "Hello!" every time the button is clicked, just like it was 
supposed to.

Passing arguments to callback functions
---------------------------------------

If we want to make multiple buttons that print different things, do we 
also need to define multiple functions that print different things?

.. code-block:: python

   def print_hello():
       print("Hello!")
   
   def print_hello_world():
       print("Hello World!")
   
   def print_hi():
       print("Hi!")
   
   ...

That's awful! If we have 15 buttons that all do the same thing with 
different texts we need to define 15 functions.

There's a better way. So far we have used the connect method like 
``some_callback.connect(function)``, but we can also use it like 
``some_callback.connect(function, arguments)``.

.. code-block:: python

   >>> def print_something(thing):
   ...     print(thing)
   ...
   >>> button = widgets.Button("Print hello")
   >>> button.on_click.connect(print_something, "Hello!")
   >>> button.on_click.run()   # BananaGUI runs print_something("Hello!")
   Hello!

Our ``print_something`` just prints whatever it gets, so we can also use 
the print function directly:

.. code-block:: python

   >>> button = widgets.Button()
   >>> button.on_click.connect(print, "Hello!")
   >>> button.on_click.run()     # BananaGUI runs print("Hello!")
   Hello!

We can also use a for loop to create a bunch of buttons easily:

.. code-block:: python

   from bananagui import load_wrapper, mainloop, widgets
   
   load_wrapper('tkinter', 'gtk3')
   
   window = widgets.Window("Button test 2")
   box = widgets.Box()
   window.add(box)
   
   for text in ["Hello!", "Hello World!", "Hi!"]:
       button = widgets.Button("Print '%s'" % text)
       button.on_click.connect(print, text)
       box.append(button)
   
   window.on_close.connect(mainloop.quit)
   mainloop.run()

Now our window has several buttons, and they all print different things.

.. code-block:: none

   ,-------------------------------.
   |  Button test 2    | _ | o | X |
   |-------------------------------|
   | ,---------------------------. |
   | |       Print 'Hello!'      | |
   | `---------------------------' |
   | ,---------------------------. |
   | |    Print 'Hello World!'   | |
   | `---------------------------' |
   | ,---------------------------. |
   | |        Print 'Hi!'        | |
   | `---------------------------' |
   `-------------------------------'

Message boxes
-------------

Now we have buttons that we can click, but they still print to the 
terminal! That's not good because we are making a GUI, and people expect 
to get message boxes instead.

There Dialog widget is a lot like the Window widget, and you can use it 
to create message boxes when needed. But the :mod:`bananagui.msgbox` 
module includes handy functions for commonly used dialogs, and it's 
often easiest to use that. This program displays a hello world message 
box when the button is clicked:

.. code-block:: python

   from bananagui import load_wrapper, mainloop, msgbox, widgets
   
   
   def say_hello(window):
       response = msgbox.info(window, "Hello World!", ["OK"])
       print("Got", repr(response))
   
   
   load_wrapper('tkinter', 'gtk3')
   
   window = widgets.Window("Test")
   button = widgets.Button("Click me")
   button.on_click.connect(say_hello, window)
   window.add(button)
   window.on_close.connect(mainloop.quit)
   mainloop.run()

The program runs like this:

.. code-block:: none

   ,-----------------------.
   |  Test     | _ | o | X |
   |-----------------------|
   | ,-------------------. |
   | |                 ,---------------.
   | |     Click me    |  Test     | X |
   | |       |\        |---------------|
   | `-------|_\-------|               |
   `----------|\-------|  Hello World! |
                       |               |
                       | ,-----------. |
                       | |    OK     | |
                       | `-----------' |
                       `---------------'

Most functions in the msgbox module return None if the user closes the
dialog or whatever the user selected otherwise. So our program prints
``Got None`` or ``Got 'OK'`` depending on how we close the hello world
dialog.
