import logging

from PIL import Image


_log = logging.getLogger(__name__)


SIZES = (
    (16, 16),
    (24, 24),
    (32, 32),
    (48, 48),
    (64, 64),
    (128, 128),
    (256, 256),
)


class Step:

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'win32') and
            (ctx.tgt_platform == 'win32')
        )

    def __call__(self, ctx, dsp):

        if ctx.icon_path.suffix.upper() != '.PNG':
            return

        build_dir = dsp.directories()['build']
        build_dir.mkdir(parents=True, exist_ok=True)

        png_path = ctx.icon_path
        ico_path = (build_dir / png_path.with_suffix('.ico').name).absolute()

        _log.info(f'Converting PNG icon at {png_path}.')

        img = Image.open(png_path)
        img.save(
            ico_path,
            format='ICO',
            sizes=SIZES,
        )

        ctx.icon_path = ico_path
        _log.info(f'Created ICO icon at {ico_path}.')
