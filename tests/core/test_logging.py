import logging

import pytest

from jormungand.core.config import config
from jormungand.core.logging import get_logger


def test_logging_set_up_for_testing():
    """Test that the testing logging configuration has been loaded"""
    logger = get_logger('root')
    assert logger.level == logging.WARNING
    assert 'testing_console_handler' in [
        handler.name for handler in logger.handlers]


def test_get_logger_returns_correct_logger():
    """Test that get_logger returns the correct logger

    See get_logger API for what the correct logger is.
    """
    logger = get_logger(__name__)
    assert logger.name == __name__
    config['default_logger_name'] = 'test_logger'
    logger = get_logger()
    assert logger.name == 'test_logger'

