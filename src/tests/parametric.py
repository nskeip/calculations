from functools import wraps
from types import FunctionType

__author__ = 'Daniel Lytkin'

def parameters(paramsList, naming = None):
    """Generates test method for every param in paramsList.
    If 'naming' argument provided, new methods are named as naming(param).
    Wrapped method must have one argument param

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
    def decorator(func): # decorator returns same function with additional attribute
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

        noNaming = attr._naming is None

        for i, param in enumerate(attr._params):
            name = attr.__name__ + str(i) if noNaming else attr._naming(param)
            def createMethod():
                testMethod = attr
                @wraps(testMethod)
                def newMethod(self):
                    return testMethod(self, param)
                # newMethod.__doc__ = testMethod.__doc__
                return newMethod

            setattr(testCase, name, createMethod())

        delattr(testCase, attr.__name__) # remove original method

    return testCase


