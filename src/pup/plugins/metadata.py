"""
PUP Plugin implementing the 'pup.metadata' step.
"""

import logging
import os
import subprocess
import sys
import tempfile

import pkginfo

from . import common


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

    def __call__(self, ctx, _dsp):

        src = ctx.src
        _log.info('Collecting metadata for %r.', src)

        with tempfile.TemporaryDirectory(prefix='pup-metadata-') as temp_dir:
            wheel_file = self._create_wheel(ctx.src, temp_dir)
            ctx.src_metadata = pkginfo.Wheel(wheel_file)

        for field in self._METADATA_FIELDS:
            _log.debug('%s=%r', field, getattr(ctx.src_metadata, field))


    def _create_wheel(self, src, work_dir):

        src_abs = os.path.abspath(src)
        cmd = [sys.executable, '-m', 'pip', 'wheel', '--no-deps', src_abs]
        
        _log.debug('About to run %r.', ' '.join(cmd))

        cwd = os.getcwd()
        try:
            os.chdir(work_dir)
            result = subprocess.run(cmd, capture_output=True)
            if result.stderr:
                common.log_lines(_log.error, 'pip stderr', result.stderr)
            common.log_lines(_log.debug, 'pip stdout', result.stdout)
            wheel_file = os.listdir()[0]
        finally:
            os.chdir(cwd)

        return os.path.join(work_dir, wheel_file)
