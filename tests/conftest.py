import os
import pytest

import bananagui


with pytest.raises(RuntimeError,
                   message="the mainloop hasn't been initialized"):
    bananagui.Window()

toolkit_name = os.environ.get('TOOLKIT_NAME', 'tkinter')
bananagui.init(toolkit_name)
