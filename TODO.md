- Create a NoSuchPropertyOrSignal exception. Right now, the tracebacks
    are not as informative as they could be:

        Traceback (most recent call last):
          ...
          File "/home/akuli/BananaGUI/bananagui/core/objectbase.py", line 33, in __prop_or_sig
            property_or_signal = getattr(property_or_signal, attribute)
        AttributeError: type object 'EntryExample' has no attribute 'minsize'

- Fix the textview bug. Run examples.textview for more info.
