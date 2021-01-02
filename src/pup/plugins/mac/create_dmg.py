"""
PUP Plugin implementing the 'mac.create-dmg' step.
"""

import logging
import os
import pathlib
import shutil

import cookiecutter
from cookiecutter import generate
try:
    # Python < 3.9
    import importlib_resources as ilr
except ImportError:
    import importlib.resources as ilr

from . import dmgbuild_settings_template



_log = logging.getLogger(__name__)



class Step:

    """
    Uses `dmgbuild` to create a DMG image of the application bundle.
    """

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'darwin') and
            (ctx.tgt_platform == 'darwin')
        )

    def __call__(self, ctx, dsp):

        app_name = ctx.nice_name or ctx.src_metadata.name
        volume_name = f'{app_name} {ctx.src_metadata.version}'
        filename = f'{volume_name}.dmg'

        settings_path = self._create_dmgbuild_settings(dsp, app_name, volume_name, filename)
        self._create_dmg_file(ctx, dsp, settings_path)
        self._deliver_dmg_file(dsp, settings_path, filename)


    def _create_dmgbuild_settings(self, dsp, app_name, volume_name, filename):

        tmpl_path = ilr.files(dmgbuild_settings_template)
        tmpl_data = {
            'cookiecutter': {
                'app_name': app_name,
                'volume_name': volume_name,
                'filename': filename,
                'app_bundle_name': f'{app_name}.app',
            }
        }

        # "Generate + Remove + Generate" motivation: cookiecutter either fails
        # if the output path exists, or overwrites it. However, it does not
        # remove pre-existing files that are no longer templated. Thus, the
        # "proper" way to ensure output is consistent without deleting the
        # whole build directory is to "Generate + Remove + Generate again".

        build_dir = dsp.directories()['build']
        result_path = generate.generate_files(tmpl_path, tmpl_data, build_dir, overwrite_if_exists=True)
        shutil.rmtree(result_path, ignore_errors=True)
        result_path = generate.generate_files(tmpl_path, tmpl_data, build_dir)

        return pathlib.Path(result_path)


    def _create_dmg_file(self, ctx, dsp, settings_path):

        # The `dmgbuild` settings file includes relative paths that require
        # us launching it with its directory as the CWD.

        cwd = os.getcwd()
        try:
            os.chdir(str(settings_path))

            cmd = [
                'dmgbuild',
                '-s', 'settings.py',
                # Both overridden in the settings file.
                'volume-name',
                'output.dmg',
            ]
            dsp.spawn(
                cmd,
                out_callable=lambda line: _log.info('dmgbuild out: %s', line),
                err_callable=lambda line: _log.info('dmgbuild err: %s', line),
            )
        finally:
            os.chdir(cwd)


    def _deliver_dmg_file(self, dsp, path, filename):

        dist_dir = dsp.directories()['dist']
        dist_dir.mkdir(exist_ok=True)

        try:
            # Move file to file instead of file to dir ensures overwrites;
            # otherwise, move fails if file exists on destination dir.
            shutil.move(
                path / filename,
                dist_dir / filename,
            )
        except OSError as exc:
            _log.error('%s', exc)
