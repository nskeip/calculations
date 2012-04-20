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
from types import FunctionType

__author__ = 'Daniel Lytkin'

def default_naming(name, param):
    try:
        for p in param:
            name += '_' + str(p)
        return name
    except TypeError:
        return name + '_' + str(param)


def parameters(paramsList, naming=default_naming):
    """Generates test method for every param in paramsList.
    If 'naming' argument provided, new methods are named as naming(name, param), where name is initial method name.
    Default naming is 'name_str(param[0])_str(param[1])_...'
    Wrapped method must have one argument 'param'.

    Usage:
    params = [1, 2, 3, 4]

    @parameters(params)
    def test_method(self, param):
        self.assertTrue(param > 0)

    # will result to

    def test_method0(self):
        self.assertTrue(1 > 0)

    def test_method1(self):
        self.assertTrue(2 > 0)

    # etc..

    @parameters(params, lambda x: "test_param"+x)
    def test_method(self, param):
        self.assertTrue(param > 0)

    # will result to

    def test_param1(self):
        self.assertTrue(1 > 0)

    # etc
    """

    def decorator(
            func): # decorator returns same function with additional attribute
        func._params = paramsList
        func._naming = naming
        return func

    return decorator


def parametrized(testCase):
    """Test case class must be decorated with @parametrized for @parameters to work for its methods
    """
    for attr in testCase.__dict__.copy().values():
        if not isinstance(attr, FunctionType) or not hasattr(attr, "_params"):
            continue

        for i, param in enumerate(attr._params):
            name = attr._naming(attr.__name__, param)

            def createMethod():
                testParams = param
                testMethod = attr

                @functools.wraps(testMethod)
                def newMethod(self):
                    return testMethod(self, testParams)

                    # newMethod.__doc__ = testMethod.__doc__

                return newMethod

            setattr(testCase, name, createMethod())

        delattr(testCase, attr.__name__) # remove original method

    return testCase


