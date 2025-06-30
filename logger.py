import settings as se
import logging


def log() -> logging.Logger:
    """
    Configure and return the root logger.

    :return: Configured root logger
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(se.FILE_LOG_NAME)
    file_handler.setLevel(logging.WARNING)
    file_formatter = logging.Formatter("%(asctime)s %(funcName)s %(levelname)s:\n\t%(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    return logger
