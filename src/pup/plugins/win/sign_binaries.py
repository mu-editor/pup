"""
PUP Plugin implementing the 'win.sign-binaries' step.
"""

import logging
import os
import pathlib
import platform



_log = logging.getLogger(__name__)



class Step:

    """
    Signs executables and shared libraries to be distributed
    using Windows SDK's signtool.exe.
    """

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'win32') and
            (ctx.tgt_platform == 'win32')
        )


    def __init__(self):

        self._identity = None
        self._signtool = None


    def __call__(self, ctx, dsp):

        try:
            self._identity = os.environ['PUP_SIGNING_IDENTITY']
        except KeyError as exc:
            _log.error('Cannot sign: environment variable %s not defined.', str(exc))
            return

        try:
            self._signtool = self._find_signtool(ctx, dsp)
        except RuntimeError as exc:
            _log.error('Cannot sign: %s.', exc)
            return

        self._sign_binaries(ctx, dsp)


    _SIGNTOOL_DIR_FROM_PYTHON_ARCH = {
        '32bit': 'x86',
        '64bit': 'x64',
    }

    def _find_signtool(self, ctx, dsp):

        # AFAICT there's no "central registry" (pun intended!)
        # where the available `signtool.exe` can be located.

        # We'll look for it under the directories defined by
        # the Windows PROGRAMFILES* environment variables.
        program_files = [
            v for k, v in os.environ.items()
            if k.upper().startswith('PROGRAMFILES')
        ]

        # Expected to be under a "../bin/<version>/" directory.
        signtool_paths = [
            path
            for pf in program_files
            for path in pathlib.Path(pf).glob('**/bin/**/signtool.exe')
        ]
        _log.debug('signtool_paths=%r', signtool_paths)

        # Figure out which, if any, apply to our architecture.
        arch, _ = platform.architecture()
        try:
            signtool_dir = self._SIGNTOOL_DIR_FROM_PYTHON_ARCH[arch]
        except KeyError:
            raise RuntimeError(f'no signtool.exe found for arch={arch!r}')

        # Sort candidates so that we can get the "most recent" one.
        signtool_paths = sorted(
            path for path in signtool_paths
            if path.parent.name.lower() == signtool_dir.lower()
        )
        _log.debug('signtool_paths=%r', signtool_paths)
        
        try:
            signtool_path = signtool_paths[-1]
        except IndexError:
            raise RuntimeError('no usable signtool.exe found')

        return signtool_path


    def _sign_binaries(self, ctx, dsp):

        for extension in ('exe', 'dll', 'pyd'):
            for path in ctx.relocatable_root.glob(f'**/*.{extension}'):
                self._sign_one_file(dsp, path)


    def _sign_one_file(self, dsp, path):

        cmd = [
            str(self._signtool),
            'sign',
            '/q',
            '/n', self._identity,
            '/fd', 'SHA256',
            # TODO: Do not hardcode this URL, grab it from an env var.
            '/tr', 'http://timestamp.digicert.com',
            '/td', 'SHA256',
            str(path)
        ]
        _log.info('Signing %r...', str(path))
        dsp.spawn(
            cmd,
            out_callable=lambda line: _log.info('signtool.exe out: %s', line),
            err_callable=lambda line: _log.info('signtool.exe err: %s', line),
        )
