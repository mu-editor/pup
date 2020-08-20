"""
PUP logging setup module.
"""

import logging



def _level_from_string(log_level_str):

    return getattr(logging, log_level_str.upper())



def start(log_level_str):
    """
    Starts logging messages of severity `log_level_str` or higher to STDERR.
    """
    logging.basicConfig(
        level=_level_from_string(log_level_str),
        format='%(asctime)s %(levelname).1s %(name)s %(message)s',
        datefmt='%Y%m%d %H%M%S',
    )
    logging.captureWarnings(True)
