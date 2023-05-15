import logging
import logging.config

from config import settings
from .utils import Singleton


class LoggingManager(metaclass=Singleton):
    """Singleton logging management class

    The LoggingManager is responsible for setting up/configuring 
    the root logger, as well as, providing logging.Logger instances.
    """

    # .. note::
    #   
    #     1. The LoggingManager might be better off being implemented as  
    #     simply module level functions. However, the assignment requirements
    #     on which this project is based required the logger to be a singleton.
    #     If necessary, it hopefully won't be too hard to refactor this in the
    #     future.
    #     2. The intent of the assignment specification was probably to make
    #     all modules use the same ``logging.Logger`` instance, however,
    #     giving each module the ability to create an instance logger that
    #     is initialized with ``get_logger(__name__)`` should make the log
    #     messages more useful for debugging.

    def __init__(self):
        self.setup_root_logger()

    def setup_root_logger(self):
        """Load/reload settings for the root logger.
        """
        logging.config.dictConfig(settings.logging)

    def get_logger(self, name=None) -> logging.Logger:
        """Get a logger object

        .. note::

            For convenience and in case of future refactoring, it is better
            not to use this method directly but use
            ``logging_manager.get_logger`` instead.

        :param name: The name of the Logger instance to create or get.
        :return: A Logger instance corresponding to the name argument.

        """
        if name is None:
            logger_ = logging.getLogger(
                    settings.get('default_logger_name', 'root'))
        else:
            logger_ = logging.getLogger(name)
        return logger_


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
    return LoggingManager().get_logger(name)

