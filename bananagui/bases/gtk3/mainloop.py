from gi.repository import GLib


class MainLoop:

    @classmethod
    def init(cls, args):
        # Gtk.main() cannot be interrupted with Ctrl+C.
        cls.__loop = GLib.MainLoop()

    @classmethod
    def run(cls):
        cls.__loop.run()

    @classmethod
    def quit(cls):
        cls.__loop.quit()
