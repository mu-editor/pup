"""
PUP Plugin implementing the 'mac.sign-app-bundle' step.
"""

import logging
import os
import subprocess

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

        self._codesign = None
        self._entitlements = None

    def __call__(self, ctx, dsp):

        build_dir = dsp.directories()['build']
        app_bundle_name = ctx.src_metadata.name
        app_bundle_path = build_dir / f'{app_bundle_name}.app'

        binaries_dir = (ctx.python_runtime_dir / ctx.python_rel_exe).parent

        self._entitlements = ilr.files(sign_resources) / 'entitlements.plist'
        codesign = subprocess.check_output('which codesign', shell=True, text=True)
        self._codesign = codesign.rstrip('\n')

        self._sign_framework_binaries(dsp, app_bundle_path)
        self._sign_shared_libs(dsp, app_bundle_path)
        self._sign_binaries(dsp, binaries_dir)
        self._sign(dsp, app_bundle_path)


    def _sign_framework_binaries(self, dsp, app_bundle_path):

        for framework_path in app_bundle_path.glob('**/*.framework'):
            for file_path in framework_path.glob('**/*'):
                if file_path.is_file() and not file_path.is_symlink():
                    self._sign(dsp, file_path)


    def _sign_shared_libs(self, dsp, app_bundle_path):

        for glob in ('*.so', '*.dylib'):
            for shlib_path in app_bundle_path.glob(f'**/{glob}'):
                self._sign(dsp, shlib_path)


    def _sign_binaries(self, dsp, binaries_dir):

        for file_path in binaries_dir.glob('*'):
            if file_path.is_file() and not file_path.is_symlink():
                self._sign(dsp, file_path)


    def _sign(self, dsp, target):

        cmd = [
            self._codesign,
            '--sign',
            os.environ.get('PUP_SIGNING_IDENTITY', '-'),
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
            out_callable=lambda line: _log.info('codesign out: %s', line),
            err_callable=lambda line: _log.info('codesign err: %s', line),
        )
