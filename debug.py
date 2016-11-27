import types


indent = ''

def debug(func):
	def result(*args, **kwargs):
		words = []
		for arg in args:
			words.append(repr(arg))
		for item in kwargs.items():
			words.append('%s=%r' % item)
		msg = ('%s.%s(%s)' % (func.__module__, func.__qualname__, ', '.join(words)))
		global indent
		indent += ' '
		print(indent, 'START', msg)
		result = func(*args, **kwargs)
		print(indent, 'DONE', msg)
		indent = indent[:-1]
		return result
	return result


def debug_class(cls):
	for name, value in list(cls.__dict__.items()):	# Copy it with list().
		if isinstance(value, types.FunctionType):
			# It's a function, let's debug it.
			setattr(cls, name, debug(value))
	return cls


class DebugMeta(type):

	def __new__(metaclass, name, bases, dictionary):
		cls = type.__new__(metaclass, name, bases, dictionary)
		debug_methods(cls)
		return cls
