"""
PUP Plugin defining macOS packaging stages.
"""


class PackagingStages:

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'darwin') and
            (ctx.tgt_platform == 'darwin')
        )

    def __call__(self, ctx):
        return (
            ('stage-1', (
                'lay-down-relocatable-python',
                'pip-install-src',
                'sign-and-notarize-like-crazy',
            )),
            ('stage-2', (
                'lay-down-application-bundle',
                'sign-more-and-notarize-oh-and-give-money-to-tim',
            )),
            ('stage-3', (
                'create-dmg',
            )),
        )
