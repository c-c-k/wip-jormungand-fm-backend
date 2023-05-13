import logging
from jormungand.logging_manager import LoggingManager


def test_logging_set_up_for_testing():
    """Test that the testing logging configuration has been loaded"""
    logger = LoggingManager().get_logger('root')
    assert logger.level == logging.WARNING
    assert 'testing_console_handler' in [
        handler.name for handler in logger.handlers]
