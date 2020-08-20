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



def package(src, *, output_format=None, ignore_plugins=()):

    _log.info('Package %r: starting.', src)

    ctx = _context(ignore_plugins)
    dsp = dispatcher.Dispatcher(ctx)

    for stage, steps in dsp.stages(ctx):
        _log.info('Stage %r: starting.', stage)
        for step in steps:
            _log.info('Step %r: starting.', step)
            _log.warning('Step %r: execution pending implementation.', step)
            _log.info('Step %r: completed.', step)
        _log.info('Stage %r: completed.', stage)

    _log.info('Package %r: completed.', src)
    return 42
