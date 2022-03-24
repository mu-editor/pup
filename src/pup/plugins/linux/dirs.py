"""
PUP Plugin defining Linux directories.
"""

import pathlib

from .. import dirs



class Directories:

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'linux') and
            (ctx.tgt_platform == 'linux')
        )

    def __call__(self, ctx, _dsp):
        return {
            **dirs.DIRS,
            'cache': pathlib.Path.home() / '.local' / 'share' / 'pup',
        }
