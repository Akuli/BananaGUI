from gi.repository import GLib


def init():
    # Gtk.main() cannot be interrupted with Ctrl+C.
    global loop
    loop = GLib.MainLoop()


def main():
    loop.run()


def quit():
    global loop
    loop.quit()
    loop = None
