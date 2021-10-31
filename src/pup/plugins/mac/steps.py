"""
PUP Plugin defining macOS packaging stages.
"""


class DMG:

    FORMAT = 'dmg'

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'darwin') and
            (ctx.tgt_platform == 'darwin')
        )

    def __call__(self, ctx, _dsp):
        return (
            'pup.python-runtime',
            'mac.app-bundle-template',
            'pup.pip-install',
            'pup.install-cleanup',
            'mac.launcher',
            'mac.sign-app-bundle',
            'mac.notarize-app-bundle',
            'mac.create-dmg',
        )



class ZIP:

    FORMAT = 'zip'

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'darwin') and
            (ctx.tgt_platform == 'darwin')
        )

    def __call__(self, ctx, _dsp):
        return (
            'pup.python-runtime',
            'mac.app-bundle-template',
            'pup.pip-install',
            'pup.install-cleanup',
            'mac.launcher',
            'mac.sign-app-bundle',
            'mac.notarize-app-bundle',
            'mac.create-zip',
        )
