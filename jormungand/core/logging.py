"""
Logging configuration and handling.

This module is a thin wrapper around the builtin logging module that
mostly just makes sure logging configuration has been loaded before handing
back logger objects.
"""
import logging
import logging.config

from .config import config

_logging_configuration_loaded: bool = False


def load_logging_configuration(logging_config: dict | None = None):
    """Load/reload configuration for the root logger.
    """
    global _logging_configuration_loaded

    if logging_config is None:
        logging.config.dictConfig(config.logging)
    else:
        logging.config.dictConfig(logging_config)
    _logging_configuration_loaded = True


def get_logger(name=None):
    """Get a logger object

    Should usually be called as:
    ``logger = logging_manager.get_logger(__name__)``

    If called with a name, gets/creates and returns a logger for
    that name.

    If called without a name argument will return a default Logger
    instance defined via ``JORMUNGAND_DEFAULT_LOGGER_NAME`` env var
    or ``default_logger_name`` configuration file setting,
    if the setting is missing, the fallback is to return the root logger.

    :param name: The name of the Logger instance to create or get.
    :return: A Logger instance corresponding to the name argument.
    """
    if not _logging_configuration_loaded:
        load_logging_configuration()
    if name is None:
        logger_ = logging.getLogger(
                config.get('default_logger_name', 'root'))
    else:
        logger_ = logging.getLogger(name)
    return logger_

