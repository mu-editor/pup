"""
PUP Plugin implementing the 'mac.app-bundle-template' step.
"""

import logging

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
    the context `python_runtime_dir`.
    """

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'darwin') and
            (ctx.tgt_platform == 'darwin')
        )

    def __call__(self, ctx, _dsp):

        app_bundle_template_path = ilr.files(app_bundle_template)

        cookiecutter_ctx = {
            'cookiecutter': {
                'app_bundle_name': 'Mu Editor',                                               
                'bundle_identifier': 'mu.codewith.mu-editor',
                'version_string': '1.1.0',
                'app_executable': 'mu-editor',
            }
        }

        generate.generate_files(app_bundle_template_path, cookiecutter_ctx, '')

        _log.warning('TODO: extract macOS app bundle template.')
        ctx.python_runtime_dir = 'fill-this-with-the-correct-abs-path'
