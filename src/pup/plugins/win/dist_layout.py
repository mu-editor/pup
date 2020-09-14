"""
PUP Plugin implementing the 'win.distribution-layout' step.
"""

import logging
import pathlib
import shutil
from urllib import parse

import cookiecutter
from cookiecutter import generate
try:
    # Python < 3.8
    import importlib_resources as ilr
except ImportError:
    import importlib.resources as ilr

from . import dist_layout_template



_log = logging.getLogger(__name__)



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

        build_dir = dsp.directories()['build']
        build_dir.mkdir(parents=True, exist_ok=True)


        tmpl_path = ilr.files(dist_layout_template)
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

        ctx.python_runtime_dir = pathlib.Path(result_path) / 'Temp'
