"""
PUP Plugin implementing the 'pup.pip-install' step.
"""

import logging
import subprocess

from . import common


_log = logging.getLogger(__name__)



class Step:

    """
    Downloads 
    """

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'darwin') or
            (ctx.pkg_platform == 'win32')
        ) and (
            (ctx.pkg_platform == ctx.tgt_platform)
        )

    def __call__(self, ctx, _dsp):

        cmd = [
            str(ctx.python_runtime_exec),
            '-m',
            'pip',
            'install',
            ctx.src,
        ]

        _log.debug('About to run %r.', ' '.join(cmd))

        result = subprocess.run(cmd, capture_output=True)
        if result.stderr:
            common.log_lines(_log.error, 'pip stderr', result.stderr)
        common.log_lines(_log.debug, 'pip stdout', result.stdout)
