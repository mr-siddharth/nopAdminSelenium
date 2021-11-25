import logging
import os
from configurations import testconfig


def get_logger():
    logger = logging.getLogger("custom_logger")

    # Adding a file handler to the logger
    f_handler = logging.FileHandler(os.path.join(testconfig.LOG_DIR, "tests.log"))
    f_format = logging.Formatter('%(asctime)s - %(filename)s:%(funcName)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)
    f_handler.setLevel(logging.INFO)
    logger.addHandler(f_handler)

    # Adding a stream handler to the logger
    s_handler = logging.StreamHandler()
    s_handler.setLevel(logging.WARNING)  # Only warning and higher level messages will be sent to the stream
    s_handler.setFormatter(f_format)  # setting the same format as the file handler
    logger.addHandler(s_handler)

    logger.setLevel(logging.INFO)

    return logger
