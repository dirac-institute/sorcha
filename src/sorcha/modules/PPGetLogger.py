import logging
import os
from datetime import datetime


def PPGetLogger(
    log_fn,
    log_format="[%(asctime)s|%(process)d] %(levelname)s [%(name)s:%(lineno)d] %(message)s",
    log_name="",
):
    """
    Initialises log and error files.

    Parameters
    -----------
    log_fn : string
        Path to file into which to save the logs.

    log_format : string, optional
        Format for log filename.
        Default = "[%(asctime)s|%(process)d] %(levelname)s [%(name)s:%(lineno)d] %(message)s",

    log_name : string, optional
        Name of log. Default = ""

    Returns
    ----------
    log : logging object
        Log object.

    """

    log = logging.getLogger(log_name)
    log_formatter = logging.Formatter(log_format)

    # comment this to suppress console output
    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(log_formatter)
    # log.addHandler(stream_handler)

    file_handler_info = logging.FileHandler(log_fn, mode="a")
    file_handler_info.setFormatter(log_formatter)
    log.addHandler(file_handler_info)

    log.setLevel(logging.INFO)

    return log
