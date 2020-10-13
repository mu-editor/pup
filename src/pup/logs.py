"""
PUP logging setup module.
"""

import os
import logging
import sys



def _level_from_string(log_level_str):

    return getattr(logging, log_level_str.upper())



_OUTPUT_TO_TTY_FORMAT = {
    False: '%(asctime)s %(levelname).1s %(name)s %(message)s',
    True: '%(levelname).1s %(message)s',
}

def start(log_level_str):
    """
    Starts logging messages of severity `log_level_str` or higher to STDERR.
    Logged messages include more detail when STDERR is not a TTY.
    """
    output_is_tty = os.isatty(sys.stderr.fileno())
    logging.basicConfig(
        level=_level_from_string(log_level_str),
        format=_OUTPUT_TO_TTY_FORMAT[output_is_tty],
        datefmt='%Y%m%d %H%M%S',
    )
    logging.captureWarnings(True)
