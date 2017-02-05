bananagui.widgets - the widget classes
======================================

.. module:: bananagui.widgets

BananaGUI uses a concept of widgets. A widget is an element of the GUI 
that the user sees. For example, if we have a BananaGUI program with a 
window and a button in it, it consists of a :class:`.Window` widget and 
a :class:`.Button` widget.

The classes inherit from each other like this:

.. graphviz::

   digraph inheritance {
      Widget -> Child -> "all other widgets";
      Widget -> Parent;
      Parent -> Bin;
      Bin -> Group;
      Child -> Group;
      Bin -> Scroller;
      Child -> Scroller;
      Bin -> Window -> Dialog;
      Parent -> Box;
      Child -> Box;
   }

Base classes
------------

These classes cannot be instantiated, but other widget classes are based 
on these. You can use these classes with :func:`isinstance` and
:func:`issubclass` or you can use their methods with other widgets that 
inherit from them.

.. autoclass:: bananagui.widgets.Widget
   :members:
.. autoclass:: bananagui.widgets.Child
   :members:
.. autoclass:: bananagui.widgets.Parent
   :members:
.. autoclass:: bananagui.widgets.Bin
   :members:

Window widgets
--------------

Almost all GUI applications have one or more windows. These classes 
allow you to create windows in BananaGUI. Note that these widgets 
inherit from :class:`.Bin`.

.. autoclass:: bananagui.widgets.Window
   :members:
.. autoclass:: bananagui.widgets.Dialog
   :members:

Labels
------

Labels are :class:`.Child` widgets that display something to the user. 

.. autoclass:: bananagui.widgets.Label
   :members:
.. autoclass:: bananagui.widgets.ImageLabel
   :members:

Buttons
-------

Buttons are :class:`.Child` widgets that display something like labels, 
but they can also be clicked.

.. autoclass:: bananagui.widgets.Button
   :members:
.. autoclass:: bananagui.widgets.ImageButton
   :members:

Layout widgets
--------------

Layout widgets are :class:`.Parent` widgets and :class:`.Child` widgets 
at the same time. These widgets allow you to add multiple widgets inside 
a :class:`.Bin` widget. There is no Layout baseclass, layout widgets 
simply inherit from Parent and Child at the same time.

Currently BananaGUI has only one layout widget:

.. autoclass:: bananagui.widgets.Box

Progress bars
-------------

These widgets display a progress bar to the user.

.. autoclass:: bananagui.widgets.Progressbar
   :members:
.. autoclass:: bananagui.widgets.BouncingProgressbar
   :members:

Text editing widgets
--------------------

These widgets display text to the user, but they also allow the user to 
edit that text.

.. autoclass:: bananagui.widgets.Entry
   :members:
.. autoclass:: bananagui.widgets.TextEdit
   :members:

Number selecting widgets
------------------------

You can use :class:`.Entry` widgets for selecting numbers, but these 
widgets are usually a better choice.

.. autoclass:: bananagui.widgets.Spinbox
.. autoclass:: bananagui.widgets.Slider

Miscellaneous widgets
---------------------

.. autoclass:: bananagui.widgets.Checkbox
   :members:
.. autoclass:: bananagui.widgets.Dummy
   :members:
.. autoclass:: bananagui.widgets.Separator
   :members:
.. autoclass:: bananagui.widgets.Scroller
   :members:
.. autoclass:: bananagui.widgets.Group
   :members:
