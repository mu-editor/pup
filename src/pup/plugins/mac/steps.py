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
            'lay-down-relocatable-python',
            'pip-install-src',
            'sign-and-notarize-like-crazy',
            'lay-down-application-bundle',
            'sign-more-and-notarize-oh-and-give-money-to-tim',
            'create-dmg',
        )
