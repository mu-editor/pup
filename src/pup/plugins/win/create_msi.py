"""
PUP Plugin implementing the 'win.create-msi' step.
"""

import logging
import pathlib
import shutil
import zipfile

import cookiecutter
from cookiecutter import generate
try:
    # Python < 3.9
    import importlib_resources as ilr
except ImportError:
    import importlib.resources as ilr

from . import msi_wsx_template



_log = logging.getLogger(__name__)



_WIX_BINARIES_URL = 'https://github.com/wixtoolset/wix3/releases/download/wix3112rtm/wix311-binaries.zip'



class Step:

    """
    Extracts a `cookiecutter`-based Windows distribution template into the
    `build` directory (template variables are sourced from the context). Sets
    the context `python_runtime_dir`, pointing to where the Python runtime
    should be copied.
    """

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'win32') and
            (ctx.tgt_platform == 'win32')
        )

    def __call__(self, ctx, dsp):

        wix_install_root = self._ensure_wix(dsp)


        build_dir = dsp.directories()['build']


        tmpl_path = ilr.files(msi_wsx_template)
        tmpl_data = {
            'cookiecutter': {
                'app_name': ctx.src_metadata.name,
                'version': ctx.src_metadata.version,
            }
        }

        # "Generate + Remove + Generate" motivation: cookiecutter either fails
        # if the output path exists, or overwrites it. However, it does not
        # remove pre-existing files that are no longer templated. Thus, the
        # "proper" way to ensure output is consistent without deleting the
        # whole build directory is to "Generate + Remove + Generate again".

        result_path = generate.generate_files(tmpl_path, tmpl_data, build_dir, overwrite_if_exists=True)
        shutil.rmtree(result_path, ignore_errors=True)
        result_path = generate.generate_files(tmpl_path, tmpl_data, build_dir)


    def _ensure_wix(self, dsp):

        wix_bin_zip = dsp.download(_WIX_BINARIES_URL)
        wix_extract_dir = pathlib.Path(wix_bin_zip).with_suffix('.extracted')

        if wix_extract_dir.exists():
            return wix_extract_dir

        wix_extract_dir.mkdir()
        with zipfile.ZipFile(wix_bin_zip) as zf:
            zf.extractall(path=wix_extract_dir)

        return wix_extract_dir
