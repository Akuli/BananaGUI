# Hello World step by step

This is the first part of the BananaGUI tutorial, and we'll create a 
Hello World program.

## What is BananaGUI?

A Graphical User Interface or **GUI** is a way to use a program without 
a terminal or a command prompt. Usually GUI's consist of one or more 
windows and different kinds of things inside the windows. Most web 
browsers, text editors, games and other programs have GUI's.

Usually GUI programs are written using a **GUI toolkit**. They take care 
of displaying windows and different things inside the windows for the 
programmer, and the programmer just needs to use the GUI toolkit from a 
programming language like Python. Some of the most popular GUI toolkits 
are tkinter, GTK+ and Qt.

On the other hand, BananaGUI is not a GUI toolkit. It's not trying to 
compete with GUI toolkits or replace them, it just provides an easy way 
to use them. You can write a GUI program using BananaGUI and then run it 
using whatever GUI toolkit you want. In other words, BananaGUI is **a 
wrapper** around GUI toolkits.

**TODO:** Installing instructions.

## The Hello World program

Our first program will display a window like this:

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

## Importing and loading BananaGUI

The first thing we need to do is to import everything we need from 
BananaGUI.

```py
from bananagui import load_wrapper, mainloop, widgets
```

Next we need to load a wrapper that wraps a GUI toolkit. The 
`load_wrapper` function takes a wrapper name as an argument and loads 
that wrapper. We can also give it more than one name, and BananaGUI will 
try to load the first wrapper, and if it fails it will try the next one 
and so on.

```py
load_wrapper('tkinter', 'gtk3')
```

If you are using Windows or OSX and you installed your Python yourself, 
BananaGUI will probably use tkinter as its GUI toolkit. If you're using 
Linux you probably don't have tkinter installed, BananaGUI will use GTK+ 
instead.

Sometimes it's handy to play around with BananaGUI without actually 
using a real GUI toolkit at all. There's a special wrapper called 
`dummy` just for that, and we'll use it later in this tutorial.

Now we are ready to create the window!

## Widgets

Like other GUI libraries, BananaGUI uses **widgets**. A widget is a part 
of the GUI. For example, if we have a window with a button in it, we 
have two widgets: the window is a widget, and the button is a widget.

The `bananagui.widgets` module contains BananaGUI's widget classes. Our 
example code displays a window with the title "Hello" and some text 
inside it. So we need two one widgets, the window and something to 
display the text.

The Window widget is used for creating windows, and Label is a widget 
for displaying text. We can create a window and add a label into it like 
this:

```py
window = widgets.Window("Hello")
label = widgets.Label("Hello World!")
window.add(label)
```

BananaGUI has two kinds of widgets:

- **Parent widgets** can have other widgets inside them. For example, 
    our window is a parent and that's why we can add a label into it.
- **Child widgets** can be added to parent widgets. Our label is a child 
    widget.

You can also use the `>>>` prompt and the dummy wrapper to experiment 
with these things:

```py
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
>>>
```

It's also possible to use other wrappers than `dummy` with the `>>>` 
prompt, but the window may not show up at all, it may be unresponsive or 
you may notice other problems. We'll learn more about this in the 
mainloop section.

## Attributes

When we created a window like `window = widgets.Window("Hello")`, the 
`"Hello"` wasn't thrown away. You can still get that or change the title 
of the window to whatever you want using `window.title`.

```py
>>> window.title
'Hello'
>>> window.title = "New title"
>>> window.title
'New title'
>>> window
<bananagui.widgets.Window object, title='New title', empty>
>>>
```

The text of the label works the same way:

```py
>>> label.text = 'New text'
>>> label
<bananagui.widgets.Label object, text='New text'>
>>>
```

Many things in BananaGUI work like this. You can give the value with an 
argument when you create the widget, or you can use an attribute to 
change it later.

## The main loop

Now our hello world program has a window object, but the window might 
not be actually visible yet. Some GUI toolkits display windows right 
away, some don't.

BananaGUI uses the GUI toolkit's main event loop. It's easy to use: 
after setting everything up, we call `mainloop.run()` and wait for 
something to stop it. When it's running, we can be sure that the user 
sees the widgets we created.

```py
mainloop.run()
```

This function is typically running for a long time. Usually everything 
before this takes just a fraction of a second, but the mainloop is 
running all the time when the program is used. It might be anything from 
a couple seconds to several hours.

So now our code looks like this:

```py
from bananagui import load_wrapper, mainloop, widgets

load_wrapper('tkinter', 'gtk3')

window = widgets.Window("Hello")
label = widgets.Label("Hello World!")
window.add(label)
mainloop.run()
```

Run this program. If everything works, then that's awesome! You have 
created your first BananaGUI application.

## Callbacks

Our hello world program has a problem. If you close the window, you'll 
notice that the main loop is still running! Unfortunately I don't have 
good instructions for killing the program because it depends a lot on 
which operating system you are using.

So we need to improve the program to stop the mainloop when the user 
closes the window. The mainloop module has a `quit()` function for 
stopping `run()`, but how can we call that when the window is closed?

BananaGUI has **callbacks** for things like this. A callback can be 
connected to a function, and then that function will be called when the 
user does something.

Our window has a callback called `on_close`, and it runs when the user 
closes the window. Let's try it out on the `>>>` prompt.

```py
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
>>>
```

Usually you don't need to use the `run()` method yourself, BananaGUI 
calls it when the user does something and runs your callbacks. So let's 
solve the window closing problem.

```py
window.on_close.connect(mainloop.quit)
```

Now our code looks like this:

```py
from bananagui import load_wrapper, mainloop, widgets

load_wrapper('tkinter', 'gtk3')

window = widgets.Window("Hello")
label = widgets.Label("Hello World!")
window.add(label)
window.on_close.connect(mainloop.quit)
mainloop.run()
```

That's it, now we have a Hello World program!
