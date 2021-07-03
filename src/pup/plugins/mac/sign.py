"""
PUP Plugin implementing the 'mac.sign-app-bundle' step.
"""

import logging
import os
import pathlib
import subprocess
import tempfile

try:
    # Python < 3.9
    import importlib_resources as ilr
except ImportError:
    import importlib.resources as ilr

from . import sign_resources



_log = logging.getLogger(__name__)



class Step:

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'darwin') and
            (ctx.tgt_platform == 'darwin')
        )


    def __init__(self):

        self._identity = None
        self._codesign = None
        self._entitlements = None

    def __call__(self, ctx, dsp):

        try:
            self._identity = os.environ['PUP_SIGNING_IDENTITY']
        except KeyError as exc:
            _log.error('Cannot sign: environment variable %s not defined.', str(exc))
            return

        build_dir = dsp.directories()['build']
        app_bundle_name = ctx.nice_name
        app_bundle_path = build_dir / f'{app_bundle_name}.app'

        binaries_dir = (ctx.python_runtime_dir / ctx.python_rel_exe).parent

        self._entitlements = ilr.files(sign_resources) / 'entitlements.plist'
        self._codesign = self._cli_command_path('codesign')

        self._sign_binaries(dsp, binaries_dir)
        self._sign_libraries(dsp, app_bundle_path)
        self._sign(dsp, app_bundle_path)

        self._assess_signing_result(dsp, app_bundle_path)


    def _cli_command_path(self, command):

        shell_command = f'which "{command}"'
        result = subprocess.check_output(shell_command, shell=True, text=True)
        return result.rstrip('\n')


    def _sign_binaries(self, dsp, binaries_dir):

        for file_path in binaries_dir.glob('*'):
            if file_path.is_file() and not file_path.is_symlink():
                self._sign(dsp, file_path)


    def _sign_libraries(self, dsp, base_path):

        self._sign_framework(dsp, base_path)
        self._sign_shared_libs(dsp, base_path)
        self._sign_bundled_zips(dsp, base_path)
        self._sign_bundled_zips(dsp, base_path, extension='whl')


    def _sign_framework(self, dsp, base_path):

        for framework_path in base_path.glob('**/*.framework'):
            for file_path in framework_path.glob('**/*'):
                if file_path.is_file() and not file_path.is_symlink():
                    self._sign(dsp, file_path)


    def _sign_shared_libs(self, dsp, base_path):

        for glob in ('*.so', '*.dylib'):
            for shlib_path in base_path.glob(f'**/{glob}'):
                self._sign(dsp, shlib_path)


    def _sign_bundled_zips(self, dsp, base_path, extension='zip'):

        for zip_path in base_path.glob(f'**/*.{extension}'):
            self._sign_zip_contents(dsp, zip_path)


    def _sign_zip_contents(self, dsp, zip_path):

        _log.info('Signing %r contents...', str(zip_path))
        build_dir = dsp.directories()['build']
        with tempfile.TemporaryDirectory(prefix='sign-zip-', dir=build_dir) as td:
            dsp.spawn([
                self._cli_command_path('unzip'),
                str(zip_path),
                '-d',
                td,
            ])
            self._sign_libraries(dsp, pathlib.Path(td))
            cwd = os.getcwd()
            # Must get absolute path before os.chdir.
            zip_path_absolute = zip_path.absolute()
            try:
                os.chdir(td)
                dsp.spawn([
                    self._cli_command_path('zip'),
                    '-qyr',
                    str(zip_path_absolute),
                    '.',
                ])
            finally:
                os.chdir(cwd)


    def _sign(self, dsp, target):

        cmd = [
            self._codesign,
            '--sign',
            self._identity,
            '--entitlements',
            str(self._entitlements),
            '--deep',
            str(target),
            '--force',
            '--options',
            'runtime',
            '--timestamp',
        ]
        _log.info('Signing %r...', str(target))
        dsp.spawn(
            cmd,
            out_callable=lambda line: _log.info('codesign| %s', line),
            err_callable=lambda line: _log.info('codesign! %s', line),
        )


    def _assess_signing_result(self, dsp, app_bundle_path):

        cmd = [
            self._cli_command_path('spctl'),
            '--assess',
            '-vvvv',
            str(app_bundle_path),
        ]
        _log.info('Assessing signing result...')
        dsp.spawn(
            cmd,
            out_callable=lambda line: _log.info('spctl| %s', line),
            err_callable=lambda line: _log.info('spctl! %s', line),
        )

        # TODO: Expect `spctl` output to be along the lines of this?
        #       build/pup/<app_bundle_name>: rejected
        #       source=Unnotarized Developer ID
        #       origin=<signing certificate cn>


    def _cli_command_path(self, command):

        shell_command = f'which "{command}"'
        result = subprocess.check_output(shell_command, shell=True, text=True)
        return result.rstrip('\n')
