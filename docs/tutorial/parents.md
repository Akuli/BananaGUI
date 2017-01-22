# Parent widgets

In the previous tutorial we created this Hello World program.

```py
from bananagui import load_wrapper, mainloop, widgets

load_wrapper('tkinter', 'gtk3')

window = widgets.Window("Hello")
label = widgets.Label("Hello World!")
window.add(label)
window.on_close.connect(mainloop.quit)
mainloop.run()
```

It displayed a window like this:

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

We learned that our window is a parent widget because it can contain 
other widgets, and the label is child widget because it can be added to 
the window. If you want to check if a widget is a parent or a child, you 
can use `isinstance` with `widgets.Parent` and `widgets.Child`:

```py
>>> from bananagui import load_wrapper, widgets
>>> load_wrapper('dummy')
>>> window = widgets.Window()
>>> isinstance(window, widgets.Parent)
True
>>> isinstance(window, widgets.Child)
False
>>> label = widgets.Label()
>>> isinstance(label, widgets.Parent)
False
>>> isinstance(label, widgets.Child)
True
>>>
```

In this tutorial we'll learn to use more Parent widgets.

## Bins

What if we want to add two labels into one window?

If you try that out on the `>>>` prompt you'll notice that the window 
doesn't like that at all.

```py
>>> window = widgets.Window("Test")
>>> window.add(widgets.Label("Test 1"))
>>> window.add(widgets.Label("Test 2"))
Traceback (most recent call last):
  ...
ValueError: there's already a child, cannot add()
>>>
```

This is because BananaGUI windows are `widgets.Bin` instances. Bin 
widgets can have one child or no children at all. This may feel stupid 
right now, but BananaGUI would be more complicated without widgets like 
this.

You can get the child of a Bin widget after adding it using the `child` 
attribute.

```py
>>> window.child
<bananagui.widgets.Label object, text='Test 1'>
>>>
```

Or you can get rid of the child using the `remove` method:

```py
>>> window
<bananagui.widgets.Window object, title='BananaGUI Window', contains a child>
>>> window.remove(window.child)
>>> window
<bananagui.widgets.Window object, title='BananaGUI Window', empty>
>>>
```

## Boxes

The window can have only one child, but it doesn't mean that there's no 
way to have two labels in it. The easiest way to do that is to create a 
Box widget, and then add the labels into the box. Let's make a program 
that creates a window like this:

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

```py
from bananagui import load_wrapper, mainloop, widgets

load_wrapper('tkinter', 'gtk3')

window = widgets.Window("Box test")
box = widgets.Box()
box.append(widgets.Label("Label 1"))
box.append(widgets.Label("Label 2"))
window.add(box)

window.on_close.connect(mainloop.quit)
mainloop.run()
```

If you run the program you'll notice that it displays two labels above 
each other, just like we wanted it to do.

You probably noticed that boxes can be added to parent widgets, and 
child widgets can be added to boxes. So are they children or parents?

```py
>>> box = widgets.Box()
>>> isinstance(box, widgets.Parent)
True
>>> isinstance(box, widgets.Child)
True
>>>
```

There we go, boxes are parents and children at the same time.

It's also possible to add widgets next to each other:

    ,---------------------------.
    |  Box test 2   | _ | o | X |
    |---------------------------|
    |             |             |
    |   Label 1   |   Label 2   |
    |             |             |
    `---------------------------'

All we need to do is to make the box horizontal using 
`bananagui.HORIZONTAL`. The boxes are vertical by default because most 
of the time we use vertical boxes more than horizontal boxes.

```py
from bananagui import load_wrapper, mainloop, widgets, HORIZONTAL

load_wrapper('tkinter', 'gtk3')

window = widgets.Window("Test")
box = widgets.Box(HORIZONTAL)
box.append(widgets.Label("Label 1"))
box.append(widgets.Label("Label 2"))
window.add(box)

window.on_close.connect(mainloop.quit)
mainloop.run()
```

You might be wondering why we add a child widget to the window using a 
method called `add`, but boxes have an `append` method instead. Lists 
also have a method called `append`, and this is not just a coincidence. 
Boxes actually behave like lists in many ways:

```py
>>> box = widgets.Box()
>>> box.append(widgets.Label("label 0"))
>>> box.append(widgets.Label("label 1"))
>>> box[0]
<bananagui.widgets.Label object, text='label 0'>
>>> box[1]
<bananagui.widgets.Label object, text='label 1'>
>>> box[:]
[<bananagui.widgets.Label object, text='label 0'>,
 <bananagui.widgets.Label object, text='label 1'>]
>>> box[::-1]
[<bananagui.widgets.Label object, text='label 1'>,
 <bananagui.widgets.Label object, text='label 0'>]
>>>
```

Boxes also have most of the methods that list have. So if you can do 
something to a list, you should be able to do the same thing to a box.
