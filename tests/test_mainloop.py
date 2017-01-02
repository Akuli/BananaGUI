# Copyright (c) 2016-2017 Akuli

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import threading
import time

import pytest

from bananagui import mainloop


def test_init_run_quit(dummywrapper):
    with pytest.raises(RuntimeError):
        # It's initialized already because loading dummywrapper
        # initialized it.
        mainloop.init()
    mainloop.quit()     # not running, does nothing

    runthread = threading.Thread(target=mainloop.run)
    runthread.daemon = True
    runthread.start()
    with pytest.raises(RuntimeError):
        mainloop.run()  # cannot have two run()s going at the same time
    mainloop.quit()
    runthread.join()

    with pytest.raises(RuntimeError):
        mainloop.run()  # needs to be initialized


def broken_callback(*args):
    assert args == (1, 2, 3)
    raise ValueError("oh shit")


def test_add_timeout(dummywrapper, capsys):
    with pytest.raises(TypeError):
        mainloop.add_timeout('hello', print)
    with pytest.raises(TypeError):
        mainloop.add_timeout(1.0, print)    # must be integer
    with pytest.raises(ValueError):
        mainloop.add_timeout(-1, print)

    # The dummywrapper uses threads to implement the timeouts, so we
    # don't need to call mainloop.run().
    mainloop.add_timeout(1, broken_callback, 1, 2, 3)
    time.sleep(0.002)    # wait for it to run

    # add_timeout should magically show the connect line in the
    # traceback.
    output, errors = capsys.readouterr()
    assert not output
    assert 'mainloop.add_timeout(1, broken_callback, 1, 2, 3)' in errors
