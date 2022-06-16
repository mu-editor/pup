"""
PUP Plugin defining macOS packaging stages.
"""


class Steps:

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'darwin') and
            (ctx.tgt_platform == 'darwin')
        )

    def __call__(self, ctx, _dsp):
        return (
            'mac.icon-from-png',
            'pup.python-runtime',
            'mac.app-bundle-template',
            'pup.pip-install',
            'pup.install-cleanup',
            'mac.launcher',
            'mac.sign-app-bundle',
            'mac.notarize-app-bundle',
            'mac.create-dmg',
        )
