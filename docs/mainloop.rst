The Main Loop
=============

BananaGUI can be in a few different states:

    - **Not loaded**: BananaGUI has just been imported. It's not ready to be
      used yet.

    - **Loaded**: :func:`bananagui.load` has been called. The mainloop is
      ready to run, but it's not running yet. Widgets can be created and
      timeouts can be added, but the timeouts aren't guaranteed to run and
      the widgets aren't guaranteed to be visible yet. Typically the
      mainloop is in this state for a short time while the widgets are being
      created.

    - **Running**: Widgets are visible and timeouts work. New widgets can be
      still made and new timeouts can be added. Applications are in this
      state most of the time.

    - **Finished**: The mainloop is not running anymore because
      :func:`bananagui.quit()` was called. Most applications exit here.

Different functions can be used for going from one state to another:

.. graphviz::

    digraph states {
        rankdir=LR;
        "Not loaded" -> Loaded [ label="load()" ];
        Loaded -> Running      [ label="run()"  ];
        Running -> Finished    [ label="quit()" ];
    }

.. autofunction:: bananagui.load
.. autofunction:: bananagui.run
.. autofunction:: bananagui.quit

Timeouts
--------

**TODO:** add some kind of explanation about blocking callbacks and why
we need timeouts instead of :func:`time.sleep`.

.. autofunction:: bananagui.add_timeout

.. data:: bananagui.RUN_AGAIN

    This can be returned from timeout callbacks, as explained above.
