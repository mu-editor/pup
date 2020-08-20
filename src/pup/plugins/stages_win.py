"""
PUP Plugin defining macOS packaging stages.
"""


class PackagingStages:

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'win32') and
            (ctx.tgt_platform == 'win32')
        )

    def __call__(self, ctx):
        return (
            ('stage-1', (
                'lay-down-relocatable-python',
                'pip-install-src',
                'sign-the-way-microsoft-needs',
            )),
            ('stage-2', (
                'create-a-clickable-thingie',
            )),
            ('stage-3', (
                'pack-it-all-into-a-single-file-artifact',
            )),
        )
