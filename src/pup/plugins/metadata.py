"""
PUP Plugin implementing the 'pup.metadata' step.
"""

import logging
import os
import pathlib
import sys

import pkginfo
import pkg_resources
import requirements


_log = logging.getLogger(__name__)



class Step:

    """
    Populates the context with source package metadata.
    """

    # Strategy
    # --------
    # Use `https://pypi.org/project/pkginfo/` to collect non-installed package
    # metadata. Its API depends on the "source kind" (sdist, wheel, etc.), so:
    #
    # - Run `pip wheel` to create a wheel file from the source.
    # - Use pkginfo wheel API to collect source package metadata.

    @staticmethod
    def usable_in(ctx):
        # Should work "everywhere".
        return True

    _METADATA_FIELDS = [
        'author',
        'author_email',
        'classifiers',
        'description',
        'description_content_type',
        'download_url',
        'home_page',
        'keywords',
        'license',
        'maintainer',
        'maintainer_email',
        'metadata_version',
        'name',
        'obsoletes',
        'obsoletes_dist',
        'platforms',
        'project_urls',
        'provides',
        'provides_dist',
        'provides_extras',
        'requires',
        'requires_dist',
        'requires_external',
        'requires_python',
        'summary',
        'supported_platforms',
        'version',
    ]

    def __call__(self, ctx, dsp):

        src = ctx.src
        _log.info('Collecting metadata for %r.', src)

        build_dir = dsp.directories()['build']
        build_dir.mkdir(parents=True, exist_ok=True)

        wheel_file = self._create_wheel(ctx.src, build_dir, dsp)
        ctx.src_wheel = wheel_file
        ctx.src_metadata = pkginfo.Wheel(wheel_file)

        for field in self._METADATA_FIELDS:
            _log.debug('%s=%r', field, getattr(ctx.src_metadata, field))

        self._collect_pup_extra_wheel_metadata( ctx)


    def _create_wheel(self, src, work_dir, dsp):

        if os.path.exists(src):
            src = os.path.abspath(src)
            _log.info(f'Packaging local project at {src!r}.')
        else:
            _log.info('Packaging from PyPI.')
        cmd = [sys.executable, '-m', 'pip', 'wheel', '--no-deps', src]
        
        _log.info('About to run %r.', ' '.join(cmd))

        cwd = os.getcwd()
        try:
            os.chdir(work_dir)
            dsp.spawn(
                cmd,
                out_callable=lambda line: _log.info('pip out: %s', line),
                err_callable=lambda line: _log.info('pip err: %s', line),
            )
            wheel_file = os.listdir()[0]
        finally:
            os.chdir(cwd)

        return os.path.join(work_dir, wheel_file)


    # HUGE HACK
    # ---------
    # Leverage supported wheel metadata on package requirements to handle
    # `pup`-usable metadata:
    # - Find requirements associated to an extra named `pup`.
    # - If their name is a `pup` paramenter...
    # - ...use its version as the parameter value.
    #
    # Examples:
    # - icon-path==./src/project/icon.png; extra='pup'
    # - nice-name==The_Project; extra='pup'

    _PUP_EXTRA_PARAMETERS = {
        'icon-path': ('icon_path', lambda s: pathlib.Path(s).absolute()),
        'license-path': ('license_path', lambda s: pathlib.Path(s).absolute()),
        'nice-name': ('nice_name', lambda s: s.replace('_', ' ')),
        'launch-module': ('launch_module', lambda s: s),
    }

    def _collect_pup_extra_wheel_metadata(self, ctx):

        # Have to use `pkg_resources` to check for the extra because
        # `requirements` does not seem to parse those correctly, as of now.

        for req_line in ctx.src_metadata.requires_dist:

            req = pkg_resources.Requirement.parse(req_line)
            if not req.marker:
                continue
            if not req.marker.evaluate(dict(extra='pup')):
                continue
            if req.name not in self._PUP_EXTRA_PARAMETERS:
                continue

            req = requirements.requirement.Requirement.parse(req_line)
            (_, value), *_ = req.specs
            ctx_attr, value_mapper = self._PUP_EXTRA_PARAMETERS[req.name]
            value = value_mapper(value)

            _log.info(f'Setting {req.name!r} to {str(value)!r}.')
            setattr(ctx, ctx_attr, value)
