# Buttons

So far we have created programs that display some text. But that's 
boring! Let's make a program that does something when we click a button.

## Using buttons

Creating a button is easy. It's a lot like creating a label, all we need 
to do is `widgets.Button("some text")`.

```py
>>> from bananagui import load_wrapper, widgets
>>> load_wrapper('dummy')
>>> button = widgets.Button("Click me!")
>>> button
<bananagui.widgets.Button object, text='Click me!'>
>>>
```

Button widgets have an `on_click` [callback](hello-world.md#callbacks), 
just like Window widgets have an `on_close` callback. It's ran when the 
button is clicked, and it does nothing by default.

```py
>>> button.on_click
<BananaGUI callback 'on_click' of bananagui.widgets.Button object>
>>>
```

So here's a program that prints hello when the user clicks the button:

```py
from bananagui import load_wrapper, mainloop, widgets

load_wrapper('tkinter', 'gtk3')

def print_hello():
    print("Hello!")

window = widgets.Window("Button test")
button = widgets.Button("Print hello")
button.on_click.connect(print_hello)
window.add(button)

window.on_close.connect(mainloop.quit)
mainloop.run()
```

The program runs like this:

    ,-------------------------------------------.
    |  Command prompt or terminal   | _ | o | X |
    |-------------------------------------------|
    | $ python3 test.py                         |
    | Hello!                                    |
    | Hello!        ,-------------------------------.
    | Hello!        |  Button test      | _ | o | X |
    |               |-------------------------------|
    |               | ,---------------------------. |
    |               | |                           | |
    |               | |                           | |
    |               | |        Print hello        | |
    |               | |              |\           | |
    |               | |              |_\          | |
    |               | `---------------|\----------' |
    |               `-------------------------------'
    |                                           |
    `-------------------------------------------'

The terminal, command prompt or whatever you're running the program from 
displays "Hello!" every time the button is clicked, just like it was 
supposed to.

## Passing arguments to callback functions

Sometimes it's useful to define one callback that does different things 
depending on which arguments it gets. So if we want to make multiple 
buttons that print different things, do we need to also define more than 
one callback function?

```py
def print_hello():
    print("Hello!")

def print_hello_world():
    print("Hello World!")

def print_hi():
    print("Hi!")

...
```

That's awful! If we have 15 buttons that all do the same thing with 
different text we don't want to have 15 functions.

There's a better way. So far we have used the connect method like 
`some_callback.connect(function)`, but we can also use it like 
`some_callback.connect(function, arguments)`. Like this:

```py
>>> def print_something(thing):
...     print(thing)
...
>>> button = widgets.Button("Print hello")
>>> button.on_click.connect(print_something, "Hello!")
>>> button.on_click.run()
Hello!
>>>
```

When we did `button.on_click.run()`, BananaGUI did 
`print_something("Hello!")`. Nice and simple. Our `print_something` just 
prints whatever it gets, so we can also do 
`button.on_click.connect(print, "Hello!")` and BananaGUI will do 
`print("Hello!")`.

If we combine that with a for loop and [a Box](parents.md#boxes), we can 
create a bunch of buttons easily:

```py
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
```

Now our window has several buttons, and they all print different things.

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
