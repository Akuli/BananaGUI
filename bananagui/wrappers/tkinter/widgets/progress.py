from tkinter import ttk

from .basewidgets import Child, run_when_ready


class Progressbar(Child):

    def create_widget(self, parent):
        return ttk.Progressbar(parent.widget)

    @run_when_ready
    def set_bouncing(self, bouncing):
        if bouncing:
            self.widget['mode'] = 'indeterminate'
            self.widget.start(20)  # Move every 20 milliseconds.
        else:
            # Unfortunately there's no better way to hide the moving
            # part of the bar when we don't want it to bounce.
            self.widget['mode'] = 'determinate'
            self.widget.stop()

    @run_when_ready
    def set_progress(self, progress):
        self.widget.stop()  # Reset it.
        step = progress * 100
        if step > 99.99:
            # The widget would go back to zero if we stepped it this
            # much.
            step = 99.99
        self.widget.step(step)


BouncingProgressbar = Progressbar
