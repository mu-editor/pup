"""
PUP Plugin implementing the 'mac.app-bundle-template' step.
"""

import logging
import pathlib
import shutil

import cookiecutter
from cookiecutter import generate
try:
    # Python < 3.9
    import importlib_resources as ilr
except ImportError:
    import importlib.resources as ilr

from . import app_bundle_template



_log = logging.getLogger(__name__)



class Step:

    """
    Extracts a `cookiecutter`-based macOS Application Bundle template into the
    `build` directory (template variables are sourced from the context). Sets
    the context `python_runtime_dir`, pointing to where the Python runtime
    should be copied.
    """

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'darwin') and
            (ctx.tgt_platform == 'darwin')
        )

    def __call__(self, ctx, dsp):

        build_dir = dsp.directories()['build']
        build_dir.mkdir(parents=True, exist_ok=True)

        tmpl_path = ilr.files(app_bundle_template)
        tmpl_data = {
            'cookiecutter': {
                'app_bundle_name': ctx.nice_name,
                'bundle_identifier': ctx.application_id,
                'version_string': ctx.src_metadata.version,
                'copyright': self._copyright_from_context(ctx),
                'launcher_name': ctx.nice_name,
                'python_version_suffix': ctx.tgt_python_version_suffix,
                'launch_module': self._launch_module_from_context(ctx),
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

        # Remove the .gitignore file in template (keeps empty dir in git).
        (pathlib.Path(result_path) / 'Contents/Resources/.gitignore').unlink()

        ctx.python_runtime_dir = (
            pathlib.Path(result_path) / 'Contents/Resources/Python'
        )


    def _copyright_from_context(self, ctx):

        author = ctx.src_metadata.author
        license = ctx.src_metadata.license

        return f'{author}, {license}'


    def _launch_module_from_context(self, ctx):

        return ctx.launch_module if ctx.launch_module else ctx.src_metadata.name
