# BananaGUI documentation

The documentation is not meant to be viewed on GitHub. [The 
tutorial](tutorial.rst) works just fine, but most other things don't.

**TODO:** add docs to akuli.github.io and link here.

You can also build the docs yourself and read them without an Internet 
connection. You also need to install 
[Graphviz](http://www.graphviz.org/) if you want a tree diagram in the 
`bananagui.widgets` documentation.

```
$ yourpython -m pip install --user sphinx
$ cd /some/path/to/BananaGUI
$ yourpython -m sphinx docs docs/_build
$ yourpython -m webbrowser docs/_build/index.html
```
