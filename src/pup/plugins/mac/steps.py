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

    def __call__(self, ctx):
        return (
            'mac.app-bundle-template',
            'python-runtime',
            'pip-install',
            # 'mac.sign-app-bundle',
            # 'mac.notarize-app-bundle',
            # 'mac.create-dmg',
        )
