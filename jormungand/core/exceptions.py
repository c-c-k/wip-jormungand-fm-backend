"""Custom exception classes for the Jormungand flight manager

"""

import re
from string import Template

from sqlalchemy.exc import IntegrityError

class DuplicateKeyError(Exception):
    def __init__(self,
                 table_name=None, orig_err_type=None, orig_msg=None,
                 *args, **kwargs):
        if isinstance(orig_err_type, IntegrityError):
            column_name, value = re.search(
                r"DETAIL:  Key \(([^)+])\)=\(([^)+])\) already exists."
                ).groups
        msg = Template(
                ':"${column_name}" primary key with a value of "${value}" '
                'already exists in "${table_name}"'
                ).substitute(table_name=table_name,
                             column_name=column_name, value=value)
        super().__init__(msg, *args, **kwargs)


# class DuplicateKeyError(Exception):
#     def __init__(self,
#                  table_name=None, column_name=None, value=None,
#                  *args, **kwargs):
#         msg = Template(
#                 '"${column_name}" primary key with a value of "${value}" '
#                 'already exists in "${table_name}"'
#                 ).substitute(table_name=table_name,
#                              column_name=column_name, value=value)
#         super().__init__(msg, *args, **kwargs)


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
        
