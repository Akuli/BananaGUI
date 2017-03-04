from tkinter import font


def get_families():
    # For some reason, some families start with a '@' on Windows. I'm
    # not sure why, but let's ignore them for now.
    return (family for family in font.families()
            if not family.startswith('@'))
