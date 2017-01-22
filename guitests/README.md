# GUI test programs

This directory contains example BananaGUI programs.

### Using the programs

If you run the programs directly from this directory, you will get an
error message saying no module named bananagui. Instead, run them from
the parent directory of this directory, and use Python's `-m` option:

    $ pwd
    /some/place/BananaGUI/guitests
    $ python3 hello_world.py
    Traceback (most recent call last):
      File "hello_world.py", line 24, in <module>
        from bananagui import mainloop, widgets
    ImportError: No module named 'bananagui'
    $ cd ..
    $ pwd
    /some/place/BananaGUI
    $ python3 -m guitests.hello_world
    (the hello world program runs)
