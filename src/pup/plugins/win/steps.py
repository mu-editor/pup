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
            'lay-down-relocatable-python',
            'pip-install-src',
            'sign-the-way-microsoft-needs',
            'create-a-clickable-thingie',
            'pack-it-all-into-a-single-file-artifact',
        )
