"""
PUP Plugin implementing the 'mac.app-bundle-template' step.
"""

import logging


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

    def __call__(self, ctx):
        _log.warning('TODO: extract macOS app bundle template.')
        ctx.python_runtime_dir = 'fill-this-with-the-correct-abs-path'
