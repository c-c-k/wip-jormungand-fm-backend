"""Singleton implementation/s.
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
