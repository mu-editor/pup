import pathlib
import tempfile
import shutil
import logging

from PIL import Image


_log = logging.getLogger(__name__)


_ICON_SIZES = (
    (16, 1),
    (16, 2),
    (32, 1),
    (32, 2),
    (128, 1),
    (128, 2),
    (256, 1),
    (256, 2),
    (512, 1),
    (512, 2),
)


class Step:

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'darwin') and
            (ctx.tgt_platform == 'darwin')
        )

    def __call__(self, ctx, dsp):

        if ctx.icon_path.suffix.upper() != '.PNG':
            return

        build_dir = dsp.directories()['build']
        build_dir.mkdir(parents=True, exist_ok=True)

        png_path = ctx.icon_path
        icns_path = (build_dir / png_path.with_suffix('.icns').name).absolute()

        _log.info(f'Converting PNG icon at {png_path}.')

        img = Image.open(png_path)
        name = png_path.stem

        with tempfile.TemporaryDirectory() as td:
            iconset_path = pathlib.Path(td) / f'{name}.iconset'
            iconset_path.mkdir()
            for size, scale in _ICON_SIZES:
                resized = img.resize(
                    size=(size*scale, size*scale), 
                    resample=Image.BICUBIC,
                )
                scale_str = '' if scale == 1 else f'@{scale}x'
                resized_path = iconset_path / f'icon_{size}x{size}{scale_str}.png'
                resized.save(resized_path, format='PNG')
            cmd = (
                shutil.which('iconutil'),
                '-c',
                'icns',
                str(iconset_path),
                '-o',
                str(icns_path),
            )
            dsp.spawn(
                cmd, 
                out_callable=lambda line: _log.info('pip out: %s', line),
                err_callable=lambda line: _log.info('pip err: %s', line),
            )

        ctx.icon_path = icns_path
        _log.info(f'Created ICNS icon at {icns_path}.')
