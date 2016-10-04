import tkinter as tk


root = None


def init():
    global root
    root = tk.Tk()
    root.withdraw()


def main():
    root.mainloop()


def quit():
    global root
    root.destroy()
    root = None
