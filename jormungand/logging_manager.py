import logging
from logging.handlers import RotatingFileHandler
from .utils import Singleton


def _standard_formater():
    formatter = logging.Formatter(
            '%(asctime)s %(levelname)-8s: %(name)s[%(lineno)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
    return formatter


def _console_handler():
    handler_ = logging.StreamHandler()
    handler_.setLevel(logging.DEBUG)
    handler_.setFormatter(_standard_formater())
    return handler_


def _rotating_file_handler():
    handler_ = RotatingFileHandler(
            filename='debug.log', mode='a', maxBytes=1000000, backupCount=3)
    handler_.setLevel(logging.DEBUG)
    handler_.setFormatter(_standard_formater())
    return handler_


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

    _default_logger_name = 'jormungand_global_logger'

    def __init__(self):
        self.setup_logger()

    def setup_logger(self):
        """Set up the root logger
        """
        logger_ = logging.getLogger()
        logger_.setLevel(logging.DEBUG)
        logger_.addHandler(_console_handler())
        logger_.addHandler(_rotating_file_handler())

    def get_logger(self, name=None) -> logging.Logger:
        """Get a logger object

        Should usually be called as:
        ``logger = LoggingManager.get_logger(__name__)``
        If called without a name argument will return a default Logger
        instance.
        :param name: The name of the Logger instance to create or get.
        :return: A Logger instance corresponding to the name argument.
        """
        if name is None:
            logger_ = logging.getLogger(self._default_logger_name)
        else:
            logger_ = logging.getLogger(name)
        return logger_


