import tkinter as tk


_root = None


def init():
    global _root
    _root = tk.Tk()
    _root.withdraw()


def main():
    _root.mainloop()


def quit():
    global _root
    _root.destroy()
    _root = None
