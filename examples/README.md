# BananaGUI examples

This directory contains example BananaGUI programs.

### Using the examples

If you run the examples directly from this directory, you will
get an error message saying no module named bananagui. Instead
run them from the parent directory of this directory, and use
Python's `-m` option:

    $ pwd
    /some/place/BananaGUI/examples
    $ python3 hello_world.py 
    Traceback (most recent call last):
      File "hello_world.py", line 28, in <module>
        import bananagui
    ImportError: No module named 'bananagui'
    $ cd ..
    $ python3 -m examples.hello_world
    (the hello world program runs)
