"""
Python Mu Packager API.
"""

import logging
import sys

from . import context
from . import dispatcher



_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())



def _context(ignore_plugins):

    return context.Context(
        ignore_plugins=ignore_plugins,
        platform=sys.platform,
        python_version=sys.version_info,
    )



def package(src, *, ignore_plugins=()):

    _log.info('Package %r: starting.', src)

    ctx = _context(ignore_plugins)
    dsp = dispatcher.Dispatcher(ctx)

    for step in dsp.steps():
        _log.info('Step %r: starting.', step)
        dsp.run_pluggable_step(step)
        _log.info('Step %r: completed.', step)

    _log.info('Package %r: completed.', src)
