"""
PUP Plugin implementing the 'pup.pip-install' step.
"""

import logging
import subprocess


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

    def __call__(self, ctx, dsp):

        cmd = [
            str(ctx.python_runtime_dir / ctx.python_rel_exe),
            '-m',
            'pip',
            'install',
            '--no-warn-script-location',
            ctx.src,
        ]

        _log.info('About to run %r.', ' '.join(cmd))

        dsp.spawn(
            cmd,
            out_callable=lambda line: _log.info('pip out: %s', line),
            err_callable=lambda line: _log.info('pip err: %s', line),
        )
