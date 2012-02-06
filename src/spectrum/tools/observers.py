__author__ = 'Daniel Lytkin'

class Observable(object):
    """Observer. Listeners must be callable, taking one argument 'item', which is the changed item
    """

    def __init__(self):
        self.__listeners = []

    def add_listener(self, listener):
        self.__listeners.append(listener)

    def remove_listener(self, listener):
        self.__listeners.remove(listener)

    @property
    def listeners(self):
        return self.__listeners

    def notify(self, item):
        for listener in self.__listeners:
            listener(item)