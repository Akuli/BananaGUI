import threading
import time

_running = False


def init():
    pass


def run():
    global _running
    _running = True
    while _running and len(threading.enumerate()) > 1:
        # There's more threads than just the main thread.
        time.sleep(0.2)


def quit():
    global _running
    _running = False


def _run_callback(sleeptime, func):
    while True:
        time.sleep(sleeptime)
        if func() is None:
            break


def add_timeout(milliseconds, callback):
    thread = threading.Thread(
        target=_run_callback,
        args=[milliseconds / 1000, callback])
    thread.start()
