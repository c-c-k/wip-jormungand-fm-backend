"""Singleton implementation/s.

This is implementation is here is here because 
the original project requirement required it
and because singletons and metaclasses sound cool.

Nevertheless it is not used in the project because:
    1. Python modules are already essentially singletons.
    2. Using global module level variables is as much a python 
       antipattern as using a singleton is.
    3. Modules are easier to mock during unittesting.
"""

class Singleton(type):
    """Singleton metaclass implementation.

    This implementation is copy/pasted from:
    https://stackoverflow.com/q/6760685
    """
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = (
                    super(Singleton, cls).__call__(*args, **kwargs)
                    )
        return cls._instances[cls]
