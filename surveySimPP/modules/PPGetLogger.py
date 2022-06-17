#!/usr/bin/python

import logging
import os
from datetime import datetime


def PPGetLogger(
        log_location,
        log_format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s ',
        log_name='',
        log_file_info='postprocessing.log',
        log_file_error='postprocessing.err'):

    # log_format     = '',
    log = logging.getLogger(log_name)
    log_formatter = logging.Formatter(log_format)

    # comment this to suppress console output
    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(log_formatter)
    # log.addHandler(stream_handler)

    dstr = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    cpid = os.getpid()

    log_file_info = str(log_location + dstr + '-p' + str(cpid) + '-' + log_file_info)
    log_file_error = str(log_location + dstr + '-p' + str(cpid) + '-' + log_file_error)

    file_handler_info = logging.FileHandler(log_file_info, mode='w')
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    log.addHandler(file_handler_info)

    file_handler_error = logging.FileHandler(log_file_error, mode='w')
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    log.addHandler(file_handler_error)

    log.setLevel(logging.INFO)

    return log
