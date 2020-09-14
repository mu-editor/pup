"""
PUP Plugin implementing the 'mac.app-bundle-template' step.
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
                'app_bundle_name': ctx.src_metadata.name,
                'bundle_identifier': self._bundle_id_from_context(ctx),
                'version_string': ctx.src_metadata.version,
                'copyright': self._copyright_from_context(ctx),
                'launcher_name': ctx.src_metadata.name,
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

        ctx.python_runtime_dir = (
            pathlib.Path(result_path) / 'Contents/Resources/Python'
        )


    def _bundle_id_from_context(self, ctx):

        # Generating application bundle_ids from the package's home_page URL
        # ------------------------------------------------------------------
        # Two sets of dot-separated strings:
        # - Reverse DNS host/domain part of URL.
        # - In order path components of URL.
        #
        # Example:
        # - home_page='https://example.com/a/path'
        # - bundle_id='com.example.a.path'

        url_parts = parse.urlsplit(ctx.src_metadata.home_page)
        return '.'.join((
            '.'.join(reversed(url_parts.netloc.split('.'))),
            '.'.join(filter(None, url_parts.path.split('/')))
        ))


    def _copyright_from_context(self, ctx):

        author = ctx.src_metadata.author
        license = ctx.src_metadata.license

        return f'{author}, {license}'


    def _launch_module_from_context(self, ctx):

        return ctx.launch_module if ctx.launch_module else ctx.src_metadata.name
