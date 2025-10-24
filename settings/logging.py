import inspect
import logging
import os
import time
import threading
from platform_info import full_platform_info
from dotenv import load_dotenv

load_dotenv()
LOGGING_CONFIG_FILE = '../config.env'
LOGGING_OUTPUT_FILE = '../logs.txt'


class CustomLoggingAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):

        frame = inspect.currentframe()
        while frame:
            if 'self' in frame.f_locals:
                class_name = frame.f_locals['self'].__class__.__name__
                break
            frame = frame.f_back
        else:
            class_name = "UnknownClass"

        extra = kwargs.get('extra', {})
        extra['className'] = class_name
        kwargs['extra'] = extra
        return msg, kwargs


def get_log_level():
    level_str = os.getenv("LOG_LEVEL", "DEBUG").upper()
    return getattr(logging, level_str, logging.DEBUG)


def setup_logger(name: str) -> CustomLoggingAdapter:
    logger = logging.getLogger(name)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - Class: %(className)s - Method: %(funcName)s - %(message)s'
        )
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(LOGGING_OUTPUT_FILE)

        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(stream_handler, file_handler)

    logger.setLevel(get_log_level())
    return CustomLoggingAdapter(logger, {})


def update_level_from_env(logger: CustomLoggingAdapter):
    load_dotenv(LOGGING_CONFIG_FILE, override=True)
    new_level = get_log_level()
    logger.logger.setLevel(new_level)
    logger.debug(full_platform_info())
    logger.debug(f"Logger level reloaded → {logging.getLevelName(new_level)}")


def auto_logger(logger: CustomLoggingAdapter, interval=10):
    """Start a background thread to reload the logging level every N seconds."""
    def watch():
        while True:
            try:
                update_level_from_env(logger)
            except Exception as e:
                logger.error(f"Error reloading log level: {e}")
            time.sleep(interval)
    threading.Thread(target=watch, daemon=True).start()
