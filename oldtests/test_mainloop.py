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

    mainloop.init()  # for other tests


def good_callback(*args):
    assert args == (1, 2, 3)
    return None


def broken_callback(*args):
    assert args == (1, 2, 3)
    raise ValueError("oh shit")


def broken_callback_2(*args):
    assert args == (1, 2, 3)
    return 123


def test_add_timeout(dummywrapper, capsys):
    with pytest.raises(ValueError):
        mainloop.add_timeout(0, print)
    with pytest.raises(ValueError):
        mainloop.add_timeout(-1, print)

    callbacks = [good_callback, broken_callback, broken_callback_2]
    brokens = [False, True, True]
    for callback, broken in zip(callbacks, brokens):
        # The dummywrapper uses threads to implement the timeouts, so
        # we don't need to call mainloop.run().
        mainloop.add_timeout(0.001, callback, 1, 2, 3)
        time.sleep(0.002)    # wait for it to run

        output, errors = capsys.readouterr()
        assert not output
        if broken:
            # add_timeout should magically show the connect line in the
            # traceback.
            assert 'mainloop.add_timeout(0.001, callback, 1, 2, 3)' in errors
        else:
            assert not errors
