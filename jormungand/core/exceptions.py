"""Custom exception classes for the Jormungand flight manager

"""

from string import Template


class DuplicateKeyError(Exception):
    def __init__(self,
                 table_name=None, column_name=None, value=None,
                 *args, **kwargs):
        msg = Template(
                '"${column_name}" primary key with a value of "${value}" '
                'already exists in "${table_name}"'
                ).substitute(table_name=table_name,
                             column_name=column_name, value=value)
        super().__init__(msg, *args, **kwargs)


class InvalidDataError(Exception):
    pass


class DataNotFoundError(Exception):
    def __init__(self,
                 table_name=None, column_name=None, value=None,
                 *args, **kwargs):
        msg = Template(
                'No entry with "${column_name}" value of "${value}" '
                'found in "${table_name}"'
                ).substitute(table_name=table_name,
                             column_name=column_name, value=value)
        super().__init__(msg, *args, **kwargs)
        
