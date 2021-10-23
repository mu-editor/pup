"""
PUP Plugin defining Linux packaging stages.
"""


class Steps:

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'linux') and
            (ctx.tgt_platform == 'linux')
        )

    def __call__(self, ctx, _dsp):
        return (
            'pup.python-runtime',
            'linux.appdir_layout',
            'pup.pip-install',
            'pup.install-cleanup',
            'linux.appdir_create',
        )
