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


class ObjectCache(type):
    """Metaclass for cache-enabled classes. It adds __call__ method to class
    objects, which is called before creating any instances, and searches the
    cache for the object creates with same arguments first.
    """
    cache = dict()

    def __call__(cls, *args, **kwargs):
        # this is called before creating any instances
        key = tuple([cls.__name__, ] + list(args) + sorted(kwargs.items()))
        instance = ObjectCache.cache.get(key)
        if instance is None:
            #noinspection PyArgumentList
            instance = type.__call__(cls, *args, **kwargs)
            ObjectCache.cache[key] = instance
        return instance


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
            raise NameError("Can't find '%s' in parents" % self.name)
        func.__doc__ = source.__doc__
        return func

doc_inherit = DocInherit


def mixin(instance, new_class):
    instance.__class__ = type(
        '{}_with_{}'.format(instance.__class__.__name__, new_class.__name__),
        (instance.__class__, new_class),
        {}
    )


class MultiModeStringFormatter:
    """This class is intended to mixin to objects that support multiple string representations, e.g. normal or
    factorized representations for Integer.
    Common modes are:
        'normal': default representation
        'latex': LaTeX-suitable representation
        'verbose': verbose representation, that is factorized for Integer, LCM-expanded for semisimple etc
        'mixed': combination of normal and verbose in form '<normal> = <verbose>'
    """
    @classmethod
    def mixin_to(cls, instance, mode='normal'):
        if not isinstance(instance, MultiModeStringFormatter):
            instance._original_str = instance.__str__
            mixin(instance, cls)
            instance.__class__.__str__ = MultiModeStringFormatter.__str__
        instance.str_mode = mode
        return instance

    def __str__(self):
        mode = self.str_mode

        if mode == 'normal':
            return self._original_str()
        elif mode == 'mixed':
            return '{normal} = {verbose}'.format(normal=self._original_str(), verbose=self.str_verbose())
        else:
            method = getattr(self, 'str_{mode}'.format(mode=mode), self._original_str)
            return method()


def trace_variable(widget, var_name, mode, callback):
    """Adds callback to tk variable
    """
    cbname = widget.register(callback)
    widget.tk.call("trace", "variable", var_name, mode, cbname)
    return cbname