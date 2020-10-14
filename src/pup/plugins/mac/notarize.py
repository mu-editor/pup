"""
PUP Plugin implementing the 'mac.notarize-app-bundle' step.
"""

import logging
import os
import subprocess
import time
import xml.etree.ElementTree as et



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
        request_uuid = self._request_notarization(ctx, dsp, app_bundle_zip, user, password)
        self._wait_notarization(dsp, request_uuid, user, password)
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


    def _parse_xml_plist(self, xml_payload):
        """
        Returns a `dict` built from parsing the XML Property List in `xml_payload`.
        """
        root_element = et.fromstring(xml_payload)
        xml_dict, *tail = root_element.findall('./dict')
        if len(tail):
            _log.warning('Multiple dicts in XML plist: %r', xml_payload)
        return self._parse_xml_dict(xml_dict)


    def _parse_xml_dict(self, element):
        """
        Returns a `dict` built from recursively parsing an XML element tree
        starting with a <dict> element, followed by key/value element pairs:
        keys are the text within <key> elements, values are the text within
        the following elements (if such elements are <dict>, the function is
        called recursively).
        """
        result = {}
        element_iter = iter(element)
        for k_element in element_iter:
            v_element = next(element_iter)
            k = k_element.text
            v = self._parse_xml_dict(v_element) if v_element.tag == 'dict' else v_element.text
            result[k] = v
        return result


    def _request_notarization(self, ctx, dsp, app_bundle_zip, user, password):

        cmd = [
            self._cli_command_path('xcrun'),
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
        xml_output_lines = []
        _log.info('Requesting notarization...')
        dsp.spawn(
            cmd,
            out_callable=xml_output_lines.append,
            err_callable=lambda line: _log.info('altool! %s', line),
        )
        xml_payload = '\n'.join(xml_output_lines)
        _log.debug('xml_payload=%r', xml_payload)
        response = self._parse_xml_plist(xml_payload)
        try:
            request_uuid = response['notarization-upload']['RequestUUID']
        except KeyError as exc:
            _log.critical('Missing %s key in notarization request output.', str(exc))
            request_uuid = None

        _log.info('Notarization request submitted: RequestUUID=%r.', request_uuid)
        return request_uuid


    def _wait_notarization(self, dsp, request_uuid, user, password, delay=60, tolerance=600):

        cmd = [
            self._cli_command_path('xcrun'),
            'altool',
            '--notarization-info',
            request_uuid,
            '--username',
            user,
            '--password',
            password,
            '--output-format',
            'xml',
        ]
        start = time.time()
        while True:
            _log.info('Requesting notarization info in %ss...', delay)
            time.sleep(delay)
            xml_output_lines = []
            dsp.spawn(
                cmd,
                out_callable=xml_output_lines.append,
                err_callable=lambda line: _log.info('altool! %s', line),
            )
            xml_payload = '\n'.join(xml_output_lines)
            _log.debug('xml_payload=%r', xml_payload)
            response = self._parse_xml_plist(xml_payload)
            response_info = response['notarization-info'] 
            try:
                status = response_info['Status']
            except KeyError as exc:
                _log.warning('Missing %s key in notarization info output.', str(exc))
            else:
                _log.info('Status is %r.', status)
            if status != 'in progress':
                break
            if time.time() - start > tolerance:
                _log.warning('Slow notarization: see https://developer.apple.com/system-status/')

        status_code = response_info['Status Code']
        status_msg = response_info['Status Message']
        log_url = response_info['LogFileURL']
        if status != 'success':
            _log.error(
                'Notarization failed: %r. Check log at %r.',
                status_msg,
                log_url,
            )
        elif status_code != '0':
            _log.warning(
                'Unexpected notarization status code %r: %r. Check log at %r.',
                status_code,
                status_msg,
                log_url,
            )


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
