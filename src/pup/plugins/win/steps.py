"""
PUP Plugin defining macOS packaging stages.
"""


class Steps:

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'win32') and
            (ctx.tgt_platform == 'win32')
        )

    def __call__(self, ctx, _dsp):
        return (
            'win.distribution-layout',
            'pup.python-runtime',
            'pup.pip-install',
            'pup.install-cleanup',
            'win.sign-binaries',
            'win.create-msi',
            'win.sign-msi',
        )
