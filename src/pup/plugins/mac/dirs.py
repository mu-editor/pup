"""
PUP Plugin defining macOS directories.
"""

import pathlib
import types

from .. import dirs



class Directories:

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'darwin') and
            (ctx.tgt_platform == 'darwin')
        )

    def __call__(self, ctx, _dsp):
        return {
            **dirs.DIRS,
            'cache': pathlib.Path.home() / 'Library' / 'Caches' / 'pup',
        }
