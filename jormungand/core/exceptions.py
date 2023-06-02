"""Custom exception classes for the Jormungand flight manager

"""


class DuplicateDataError(Exception):
    pass


class InvalidDataError(Exception):
    pass


class DataNotFoundError(Exception):
    pass
