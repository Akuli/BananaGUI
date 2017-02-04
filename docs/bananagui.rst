The top level bananagui module - general constants and functions
================================================================

.. module:: bananagui

.. autofunction:: bananagui.load_wrapper
.. autodata:: bananagui.WRAPPERS

.. The enum docs are not in the docstrings because better enum support 
   might be added to Sphinx later and these would break.

.. class:: Orient

   An :class:`enum.IntEnum` that represents an orientation.

   This enum has two members, *HORIZONTAL* and *VERTICAL*.

.. class:: Align

   An :class:`enum.IntEnum` that represents how something is aligned.

   This enumeration has these members:

   +--------+-----------------------------------+
   | LEFT   | Align to beginning.               |
   +--------+-----------------------------------+
   | CENTER | Center between beginning and end. |
   +--------+-----------------------------------+
   | RIGHT  | Align to end.                     |
   +--------+-----------------------------------+

   These aliases can be used instead with vertical things:

   +--------+-----------------------+
   | TOP    | Equivalent to LEFT.   |
   +--------+-----------------------+
   | BOTTOM | Equivalent to RIGHT.  |
   +--------+-----------------------+

.. autodata:: bananagui.RUN_AGAIN
