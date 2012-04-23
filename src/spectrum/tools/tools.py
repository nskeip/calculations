"""
Copyright 2012 Daniel Lytkin.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""

import functools
import platform

__author__ = 'Daniel Lytkin'

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

        @functools.wraps(self.mthd, assigned=('__name__', '__module__'))
        def f(*args, **kwargs):
            return self.mthd(obj, *args, **kwargs)

        return self.use_parent_doc(f, overridden)

    def get_no_inst(self, cls):
        overridden = None
        for parent in cls.__mro__[1:]:
            overridden = getattr(parent, self.name, None)
            if overridden: break

        @functools.wraps(self.mthd, assigned=('__name__', '__module__'))
        def f(*args, **kwargs):
            return self.mthd(*args, **kwargs)

        return self.use_parent_doc(f, overridden)

    def use_parent_doc(self, func, source):
        if source is None:
            raise NameError, ("Can't find '%s' in parents" % self.name)
        func.__doc__ = source.__doc__
        return func

doc_inherit = DocInherit


class StringViewFormatter(object):
    """This class wraps Integer, SpectraElement, Group, Field etc. instances
    and provides some string formatting methods (Factorized view, LaTeX view
    etc.)
    Modes:
        NORMAL - regular str(object)
        VERBOSE - factorised for integer, lcm for spectra element etc
        LATEX - latex-compatible text
        MIXED - 'NORMAL = VERBOSE'
    """
    NORMAL = 0
    VERBOSE = 1
    LATEX = 2
    MIXED = 3

    def __init__(self, object_, mode=0):
        self._object = object_
        self.mode = mode

        self._modes = {0: self.str_normal,
                       1: self.str_verbose,
                       2: self.str_latex,
                       3: self.str_mixed}

    @property
    def object(self):
        return self._object

    def str_normal(self):
        return str(self._object)

    def str_verbose(self):
        try:
            return self._object.str_verbose()
        except AttributeError:
            return str(self._object)

    def str_latex(self):
        try:
            return self._object.str_latex()
        except AttributeError:
            return str(self._object)

    def str_mixed(self):
        return self.str_normal() + " = " + self.str_verbose()

    def __str__(self):
        return self._modes[self.mode]()


def trace_variable(widget, var_name, mode, callback):
    """Adds callback to tk variable
    """
    cbname = widget.register(callback)
    widget.tk.call("trace", "variable", var_name, mode, cbname)
    return cbname