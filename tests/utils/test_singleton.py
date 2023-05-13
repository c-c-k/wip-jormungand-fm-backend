"""Test/s for the singleton implementation/s in utils/singleton.
"""

from jormungand.utils import Singleton


class SingletonClass(metaclass=Singleton):
    """Simple singleton class for testing"""

    def __init__(self, arg):
        self.init_arg = arg

    def __call__(self, arg):
        return arg


def test_singleton_is_singleton():
    """Verify that a singleton class behaves like a singleton.

    The definition of how a singleton class should behave is retroactively
    based on how it has been implemented, the definition is:
        - All invocations of the singleton class return the same instance.
        - The first call to the singleton class initializes it.
        - The first call to the singleton class uses the call parameters.
        - All following calls to the singleton class do not reinitialize it.
        - All following calls to the singleton class discard the parameters.
    """
    singleton_class_object_1 = SingletonClass(1)
    singleton_class_object_2 = SingletonClass(2)
    assert singleton_class_object_1 is singleton_class_object_2
    assert singleton_class_object_2.init_arg == 1
    assert singleton_class_object_1 not in [1, 2]
    assert singleton_class_object_1(3) == 3

