"""
PUP Plugin implementing the 'mac.launcher' step.
"""

import logging
import os
import shutil


_log = logging.getLogger(__name__)



class Step:

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'darwin') and
            (ctx.tgt_platform == 'darwin')
        )

    def __call__(self, ctx, dsp):

        build_dir = dsp.directories()['build']
        app_bundle_name = ctx.nice_name
        launcher_path = build_dir / f'{app_bundle_name}.app' / 'Contents' / 'MacOS'

        cwd = os.getcwd()
        try:
            os.chdir(launcher_path)
            dsp.spawn([
                shutil.which('clang'),
                '-mmacosx-version-min=10.9',
                '-o',
                ctx.nice_name,
                'launcher.c',
            ])
            os.unlink('launcher.c')
        finally:
            os.chdir(cwd)

        python_abs_path = ctx.python_runtime_dir / ctx.python_rel_exe
        python_abs_path.rename(python_abs_path.parent / ctx.nice_name)
