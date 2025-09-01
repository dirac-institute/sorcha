import logging
import os
from datetime import datetime


def sorchaGetLogger(
    log_location,
    log_stem,
    log_format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s ",
    log_name="",
    log_file_info="sorcha.log",
    log_file_error="sorcha.err",
):
    """
    Initialises log and error files.

    Parameters
    -----------
    log_location : string
        Filepath to directory in which to save logs.

    log_stem : string
        String output stem used to prefix all Sorcha outputs.

    log_format : string, default="%(asctime)s %(name)-12s %(levelname)-8s %(message)s "
        Format for log filename.

    log_name : string, default=""
        Name of log.

    log_file_info : string, default="sorcha.log"
        Suffix and extension with which to save info log.

    log_file_error : string, optional, default="sorcha.err"
        Suffix and extension with which to save error log.

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

    dstr = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    cpid = os.getpid()

    log_file_info = os.path.join(log_location, "-".join([log_stem, dstr, "p" + str(cpid), log_file_info]))
    log_file_error = os.path.join(log_location, "-".join([log_stem, dstr, "p" + str(cpid), log_file_error]))

    file_handler_info = logging.FileHandler(log_file_info, mode="w")
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    log.addHandler(file_handler_info)

    file_handler_error = logging.FileHandler(log_file_error, mode="w")
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    log.addHandler(file_handler_error)

    log.setLevel(logging.INFO)

    return log
