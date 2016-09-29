import tkinter as tk


class MainLoop:

    @classmethod
    def init(cls):
        cls.__root = tk.Tk()
        cls.__root.withdraw()

    @classmethod
    def run(cls):
        cls.__root.mainloop()

    @classmethod
    def quit(cls):
        cls.__root.destroy()
