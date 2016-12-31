import threading

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


def test_add_timeout(dummywrapper):
    with pytest.raises(TypeError):
        mainloop.add_timeout('hello', print)

    with pytest.raises(TypeError):
        mainloop.add_timeout(1.0, print)    # must be integer

    with pytest.raises(ValueError):
        mainloop.add_timeout(-1, print)
