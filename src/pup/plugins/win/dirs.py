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
            (ctx.pkg_platform == 'win32') and
            (ctx.tgt_platform == 'win32')
        )

    def __call__(self, ctx, _dsp):
        return {
            **dirs.DIRS,
            'cache': pathlib.Path.home() / 'AppData' / 'Local' / 'pup',
        }
