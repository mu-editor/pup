"""
PUP Plugin implementing the 'pup.install-cleanup' step.
"""

import logging
import shutil


_log = logging.getLogger(__name__)



class Step:


    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'darwin') or
            (ctx.pkg_platform == 'win32')
        ) and (
            (ctx.pkg_platform == ctx.tgt_platform)
        )

    def __call__(self, ctx, dsp):

        self._delete_test_packages(ctx)
        self._delete_platform_config(ctx)
        self._compile_lib(ctx, dsp)


    def _delete_test_packages(self, ctx):

        for test_package in ctx.python_test_packages:
            test_package_path = test_package.replace('.', '/')
            shutil.rmtree(
                str(ctx.python_runtime_dir / ctx.python_rel_stdlib / test_package_path),
                ignore_errors=True,
            )

    def _delete_platform_config(self, ctx):

        if not ctx.stdlib_platform_config:
            return
        shutil.rmtree(str(ctx.python_runtime_dir / ctx.stdlib_platform_config), ignore_errors=True)


    def _compile_lib(self, ctx, dsp):

        # Compiles both the Standard Library and Site Packages.

        python_exe = ctx.python_runtime_dir / ctx.python_rel_exe
        python_stdlib = ctx.python_runtime_dir / ctx.python_rel_stdlib

        compile_cmd = [
            str(python_exe),
            '-m',
            'compileall',
            '-l',
            '-f',
            '-q',
            '-b',
            None
        ]

        for each in python_stdlib.glob('**'):
            compile_cmd[-1] = str(each)
            dsp.spawn(
                compile_cmd,
                out_callable=lambda line: _log.info('compile out: %s', line),
                err_callable=lambda line: _log.info('compile err: %s', line),
            )
