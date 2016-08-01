"""Simple wrapper for GUI frameworks."""

import importlib


class MissingFeatureWarning(UserWarning):
    """Warned when a GUI toolkit doesn't have the requested feature."""


def get(*toolkit_names):
    """Attempt to return a toolkit from toolkit_names.

    The first one is returned, and if it's not avaliable the next one is
    etc.
    """
    if not toolkit_names:
        raise ValueError("no toolkit names were specified")
    for name in toolkit_names:
        try:
            return importlib.import_module(
                '{}.wrappers.{}'.format(__name__, name))
        except ImportError:
            pass
    raise ImportError("cannot import any of the required toolkits")
