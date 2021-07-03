"""
PUP Plugin implementing the 'mac.notarize-app-bundle' step.
"""

import contextlib
import logging
import os
import shutil
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

        build_dir = dsp.directories()['build']
        app_bundle_name = ctx.nice_name
        app_bundle_path = build_dir / f'{app_bundle_name}.app'

        app_bundle_zip = self._create_app_bundle_zip(dsp, app_bundle_path)
        request_uuid = self._request_notarization(ctx, dsp, app_bundle_zip, user, password)
        self._wait_notarization(dsp, request_uuid, user, password)
        self._staple_app_bundle(dsp, app_bundle_path)
        self._assess_notarization_result(dsp, app_bundle_path)
        app_bundle_zip.unlink()


    @contextlib.contextmanager
    def _working_directory(self, directory):

        cwd = os.getcwd()
        os.chdir(directory)
        try:
            yield
        finally:
            os.chdir(cwd)


    def _create_app_bundle_zip(self, dsp, app_bundle_path):

        with self._working_directory(app_bundle_path.parent):
            dsp.spawn(
                command=[
                    shutil.which('zip'),
                    '-qyr',
                    f'{app_bundle_path.name}.zip',
                    str(app_bundle_path.name),
                ]
            )

        return app_bundle_path.with_suffix('.app.zip')


    def _parse_xml_plist(self, xml_payload):
        """
        Returns a `dict` built from parsing the XML Property List in `xml_payload`.
        """
        root_element = et.fromstring(xml_payload)
        xml_dict, *tail = root_element.findall('./dict')
        if tail:
            _log.warning('Multiple dicts in XML plist: %r', xml_payload)
        return self._parse_xml_dict(xml_dict)


    def _parse_xml_dict(self, element):
        """
        Returns a `dict` built from recursively parsing an XML element tree
        starting with a <dict> element, containing key+value element pairs:
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

        _log.info('Submitting notarization request...')
        cmd = [
            shutil.which('xcrun'),
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
            shutil.which('xcrun'),
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


    def _staple_app_bundle(self, dsp, app_bundle_path):

        _log.info('Stapling...')
        cmd = [
            shutil.which('xcrun'),
            'stapler',
            'staple',
            app_bundle_path.name,
        ]
        with self._working_directory(app_bundle_path.parent):
            dsp.spawn(
                cmd,
                out_callable=lambda line: _log.info('stapler| %s', line),
                err_callable=lambda line: _log.info('stapler! %s', line),
            )


    def _assess_notarization_result(self, dsp, app_bundle_path):

        _log.info('Assessing notarization result...')
        cmd = [
            shutil.which('spctl'),
            '--assess',
            '-vvvv',
            str(app_bundle_path),
        ]
        dsp.spawn(
            cmd,
            out_callable=lambda line: _log.info('spctl| %s', line),
            err_callable=lambda line: _log.info('spctl! %s', line),
        )

        # TODO: Expect `spctl` output to be along the lines of this?
        #       build/pup/<app_bundle_name>: accepted
        #       source=Notarized Developer ID
        #       origin=<signing certificate cn>
