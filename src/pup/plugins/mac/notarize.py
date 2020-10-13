"""
PUP Plugin implementing the 'mac.notarize-app-bundle' step.
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


    def __call__(self, ctx, dsp):

        try:
            user = os.environ['PUP_NOTARIZE_USER']
            password = os.environ['PUP_NOTARIZE_PASSWORD']
        except KeyError as exc:
            _log.error('Cannot notarize: environment variable %s not defined.', str(exc))
        else:
            self._notarize(ctx, dsp, user, password)


    def _notarize(self, ctx, dsp, user, password):


        app_bundle_zip = self._create_app_bundle_zip(ctx, dsp)
        request_id = self._request_notarization(ctx, dsp, app_bundle_zip, user, password)
        self._wait_notarization(dsp, request_id)
        self._staple_app_bundle(dsp)


    def _cli_command_path(self, command):

        shell_command = f'which "{command}"'
        result = subprocess.check_output(shell_command, shell=True, text=True)
        return result.rstrip('\n')


    def _create_app_bundle_zip(self, ctx, dsp):

        build_dir = dsp.directories()['build']
        app_bundle_name = f'{ctx.src_metadata.name}.app'
        app_bundle_zip = f'{app_bundle_name}.zip'

        zip_path = self._cli_command_path('zip')

        orig_cwd = os.getcwd()
        try:
            os.chdir(build_dir)
            dsp.spawn(
                command=[
                    zip_path,
                    '-qyr',
                    app_bundle_zip,
                    str(app_bundle_name)
                ]
            )
        finally:
            os.chdir(orig_cwd)

        return build_dir / app_bundle_zip


    def _request_notarization(self, ctx, dsp, app_bundle_zip, user, password):

        xcrun = self._cli_command_path('xcrun')

        cmd = [
            xcrun,
            'altool',
            '--notarize-app',
            '--primary-bundle-id',
            ctx.application_id,
            '--username',
            user,
            '--password',
            password,
            '--output-format',
            'xml',
            '--file',
            app_bundle_zip,
        ]
        _log.info('Requesting notarization...')
        dsp.spawn(
            cmd,
            out_callable=lambda line: _log.info('altool| %s', line),
            err_callable=lambda line: _log.info('altool! %s', line),
        )


    def _wait_notarization(self, dsp, request_id):

        _log.info('TODO: wait notarization')


    def _staple_app_bundle(self, dsp):

        _log.info('TODO: staple app bundle')


    def _assess_notarization_result(self, dsp, app_bundle_path):

        cmd = [
            self._cli_command_path('spctl'),
            '--assess',
            '-vvvv',
            str(app_bundle_path),
        ]
        _log.info('Assessing notarization result...')
        dsp.spawn(
            cmd,
            out_callable=lambda line: _log.info('spctl| %s', line),
            err_callable=lambda line: _log.info('spctl! %s', line),
        )
        # TODO: Expect notarized to be output?
