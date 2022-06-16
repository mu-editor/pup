"""
Pluggable Micro Packager API.
"""

import logging
import sys

from . import context
from . import dispatcher



_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())



def _context(
    ignore_plugins,
    src=None,
    python_version=None,
    launch_module=None,
    launch_pyflags=None,
    nice_name=None,
    icon_path=None,
    license_path=None,
):

    return context.Context(
        src=src,
        launch_module=launch_module,
        launch_pyflags=launch_pyflags,
        nice_name=nice_name,
        icon_path=icon_path,
        license_path=license_path,
        ignore_plugins=ignore_plugins,
        platform=sys.platform,
        python_version=python_version,
    )



def package(
    src,
    *,
    ignore_plugins=(),
    python_version=None,
    launch_module=None,
    launch_pyflags=None,
    nice_name=None,
    icon_path=None,
    license_path=None,
):

    _log.info('Package %r: starting.', src)

    ctx = _context(ignore_plugins, src, python_version, launch_module, launch_pyflags, nice_name, icon_path, license_path)
    dsp = dispatcher.Dispatcher(ctx)

    dsp.collect_src_metadata()

    for step in dsp.steps():
        _log.info('Step %r: starting.', step)
        dsp.run_pluggable_step(step)
        _log.info('Step %r: completed.', step)

    _log.info('Package %r: completed.', src)



def directories(*, ignore_plugins=()):

    ctx = _context(ignore_plugins)
    dsp = dispatcher.Dispatcher(ctx)

    return dsp.directories()



def download(url, *, ignore_plugins=()):

    ctx = _context(ignore_plugins)
    dsp = dispatcher.Dispatcher(ctx)

    return dsp.download(url)
