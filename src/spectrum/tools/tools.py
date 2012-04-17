from Tkinter import  Variable
import platform

__author__ = 'Daniel Lytkin'

from functools import wraps

IS_MAC = platform.system() == "Darwin"

class DocInherit(object):
    """doc_inherit decorator

    Usage:

    class Foo(object):
        def foo(self):
            "Frobber"
            pass

    class Bar(Foo):
        @doc_inherit
        def foo(self):
            pass

    Now, Bar.foo.__doc__ == Bar().foo.__doc__ == Foo.foo.__doc__ == "Frobber"
    """

    def __init__(self, mthd):
        self.mthd = mthd
        self.name = mthd.__name__

    def __get__(self, obj, cls):
        if obj:
            return self.get_with_inst(obj, cls)
        else:
            return self.get_no_inst(cls)

    def get_with_inst(self, obj, cls):
        overridden = getattr(super(cls, obj), self.name, None)

        @wraps(self.mthd, assigned=('__name__', '__module__'))
        def f(*args, **kwargs):
            return self.mthd(obj, *args, **kwargs)

        return self.use_parent_doc(f, overridden)

    def get_no_inst(self, cls):
        overridden = None
        for parent in cls.__mro__[1:]:
            overridden = getattr(parent, self.name, None)
            if overridden: break

        @wraps(self.mthd, assigned=('__name__', '__module__'))
        def f(*args, **kwargs):
            return self.mthd(*args, **kwargs)

        return self.use_parent_doc(f, overridden)

    def use_parent_doc(self, func, source):
        if source is None:
            raise NameError, ("Can't find '%s' in parents" % self.name)
        func.__doc__ = source.__doc__
        return func

doc_inherit = DocInherit


class Properties(object):
    """This class is like dictionary, but can contain StringVars and IntVars.
    If the property 'x' is a StringVar or IntVar, then Properties['x'] will
     call get() method of the variable; Properties['x'] = y will call set()
     method.
    If 'x' is some other type, then Properties['x'] will return or substitute
     the value like the regular dictionary.

     To add a property as Variable, use add_variable() method.
     For other properties use Properties['key'] = value
    """

    def __init__(self):
        self._dict = dict()

    def __getitem__(self, item):
        value = self._dict[item]
        if isinstance(value, Variable):
            return value.get()
        return value

    def __setitem__(self, key, value):
        previous = self._dict.get(key)
        if isinstance(previous, Variable):
            previous.set(value)
        else:
            # None or not Variable
            self._dict[key] = value

    def __delitem__(self, key):
        del self._dict[key]

    def add_variable(self, key, variable, initial=None):
        self._dict[key] = variable
        if initial is not None:
            variable.set(initial)

    def get_variable(self, key):
        """Returns Variable instance for the given key. Raises ValueError if
        Properties[key] is not a Variable instance.
        """
        value = self._dict[key]
        if not isinstance(value, Variable):
            raise ValueError(
                "Entry with key '{}' is not a Variable instance.".format(key))
        return value


properties = Properties()
