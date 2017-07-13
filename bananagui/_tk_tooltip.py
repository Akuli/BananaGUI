import tkinter as tk


class _TooltipManager:
    """Tooltips for tkinter.

    License notice: This class has nothing to do with idlelib.ToolTip. I
    didn't copy-paste this from idlelib and I didn't read idlelib's
    tooltip.py when I wrote this. I wrote my own tooltip manager mainly
    because I didn't have the time to find out how I'm allowed to use
    idlelib's code.
    """

    # This needs to be shared by all instances because there's only one
    # mouse pointer.
    tipwindow = None

    def __init__(self, widget):
        widget.bind('<Enter>', self.enter, add=True)
        widget.bind('<Leave>', self.leave, add=True)
        widget.bind('<Motion>', self.motion, add=True)
        self.widget = widget
        self.got_mouse = False
        self.text = None

    @classmethod
    def destroy_tipwindow(cls, event=None):
        if cls.tipwindow is not None:
            cls.tipwindow.destroy()
            cls.tipwindow = None

    def enter(self, event):
        # For some reason, toplevels get also notified of their
        # childrens' events.
        if event.widget is self.widget:
            self.destroy_tipwindow()
            self.got_mouse = True
            self.widget.after(1000, self.show)

    def leave(self, event):
        if event.widget is self.widget:
            self.destroy_tipwindow()
            self.got_mouse = False

    def motion(self, event):
        self.mousex = event.x_root
        self.mousey = event.y_root

    def show(self):
        if not self.got_mouse:
            return

        self.destroy_tipwindow()
        if self.text is not None:
            tipwindow = type(self).tipwindow = tk.Toplevel()
            tipwindow.geometry('+%d+%d' % (self.mousex+10, self.mousey-10))
            tipwindow.bind('<Motion>', self.destroy_tipwindow)
            tipwindow.overrideredirect(True)

            # If you modify this, make sure to always define either no
            # colors at all or both foreground and background. Otherwise
            # the label will have light text on a light background or
            # dark text on a dark background on some systems.
            tk.Label(tipwindow, text=self.text, border=3,
                     fg='black', bg='white').pack()


def set_tooltip(widget, text):
    if text is None:
        if hasattr(widget, '_tooltip_manager'):
            widget._tooltip_manager.text = None
    else:
        if not hasattr(widget, '_tooltip_manager'):
            widget._tooltip_manager = _TooltipManager(widget)
        widget._tooltip_manager.text = text
