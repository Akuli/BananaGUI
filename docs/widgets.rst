The Widgets
===========

.. module: bananagui

See :ref:`tut-widgets` in the tutorial for a description of what widgets are.

The widget classes inherit from each other like this:

.. graphviz::

    digraph inheritance {
        Widget -> "all other widgets";
        Widget -> Parent -> Bin -> Window -> Dialog;
    }

Window widgets
--------------

Almost all GUI applications have one or more windows. These classes 
allow you to create windows in BananaGUI. Note that these widgets 
inherit from :class:`.Bin`.

.. autoclass:: bananagui.Window
   :members:
.. autoclass:: bananagui.Dialog
   :members:

Labels
------

Labels are widgets that display something to the user.

.. autoclass:: bananagui.Label
   :members:

Buttons
-------

Buttons display text like labels, but they can also be clicked.

.. autoclass:: bananagui.Button
   :members:

Custom Widgets
--------------

These classes cannot be instantiated, but other widget classes are based 
on these. You can use these classes with :func:`isinstance` and
:func:`issubclass` or you can use their methods with other widgets that 
inherit from them.

.. autoclass:: bananagui.Widget
   :members:
.. autoclass:: bananagui.Parent
   :members:
.. autoclass:: bananagui.Bin
   :members:
