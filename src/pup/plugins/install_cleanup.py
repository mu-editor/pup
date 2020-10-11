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
        self._delete_unneeded_scripts(ctx)
        self._delete_unneeded_paths(ctx)
        self._delete_unneeded_files(ctx)
        self._compile_lib(ctx, dsp)


    def _delete_test_packages(self, ctx):

        _log.info('Deleting Standard Library test packages...')
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


    def _delete_unneeded_scripts(self, ctx):

        python_exe = ctx.python_runtime_dir / ctx.python_rel_exe
        python_scripts_path =  ctx.python_runtime_dir / ctx.python_rel_scripts

        for file_path in python_scripts_path.glob('*'):
            if file_path == python_exe:
                continue
            if file_path.is_dir():
                shutil.rmtree(str(file_path), ignore_errors=True)
            elif not file_path.is_symlink() or file_path.resolve() != python_exe:
                # Delete any file that doesn't symlink to the Python executable.
                file_path.unlink()


    def _delete_unneeded_paths(self, ctx):

        paths_to_keep = {
            ctx.python_runtime_dir / rel_path
            for rel_path in (
                ctx.python_rel_stdlib,
                ctx.python_rel_site_packages,
                ctx.python_rel_scripts,
                'DLLs',
                'Tcl',
            )
        }

        for candidate in ctx.python_runtime_dir.iterdir():
            candidate_path = ctx.python_runtime_dir / candidate
            if not candidate_path.is_dir():
                continue
            if candidate_path in paths_to_keep:
                continue
            # Don't delete if candidate_path is parent of any of paths_to_keep.
            if any(candidate_path == parent for p in paths_to_keep for parent in p.parents):
                continue
            _log.info('Deleting %r...', str(candidate_path))
            shutil.rmtree(
                str(candidate_path),
                ignore_errors=True,
            )


    _GLOBS_TO_DELETE = (
        '*.lib',
        '*.pdb',
        '*.a',
    )

    def _delete_unneeded_files(self, ctx):

        for glob in self._GLOBS_TO_DELETE:
            _log.info('Deleting %r files...', glob)
            for file_path in ctx.python_runtime_dir.glob(f'**/{glob}'):
                file_path.unlink()


    _DONT_COMPILE_NAMES = {
        '__pycache__',
        'EGG-INFO',
    }

    _DONT_COMPILE_SUFFIXES = {
        '.dist-info',
        '.egg-info',
    }

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

        for lib_dir_path in python_stdlib.glob('**'):
            if lib_dir_path.name in self._DONT_COMPILE_NAMES:
                continue
            if lib_dir_path.suffix in self._DONT_COMPILE_SUFFIXES:
                continue
            compile_cmd[-1] = str(lib_dir_path)
            _log.info('Compiling %r...', str(lib_dir_path))
            dsp.spawn(
                compile_cmd,
                out_callable=lambda line: _log.info('compile out: %s', line),
                err_callable=lambda line: _log.info('compile err: %s', line),
            )
