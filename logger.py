import settings as se
import user_interface as ui
import logging
from functools import wraps


logging.basicConfig(
    filename=se.FILE_LOG_NAME,
    level=logging.WARNING,
    format="%(asctime)s %(funcName)s %(levelname)s:\n\t%(message)s\n",
    encoding="utf-8"
)


def log_error(display=True):
    """
    Decorator that wraps a function to catch and handle exceptions.

    :param display: Whether to display the error message to the user interface.
    :return: Decorated function that wraps exception handling logic.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                if display:
                    ui.error_print(error)
                if isinstance(error, ValueError | TypeError):
                    logging.warning(error)
                else:
                    logging.critical(error)
                    ui.exit_print()
        return wrapper
    return decorator


def handle_error(error) -> None:
    """
    Logs the provided error with a WARNING level and notifies the user of an invalid choice.

    :param error: The error or exception to be logged.
    """
    logging.warning(error)
    ui.invalid_choice(str(error))
