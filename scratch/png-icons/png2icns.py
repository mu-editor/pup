import pathlib
import tempfile
import shutil
import subprocess
import sys

from PIL import Image


SIZES = [
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
]


def create_icns(png_path):

    img = Image.open(png_path)
    name = png_path.stem

    with tempfile.TemporaryDirectory() as td:
        iconset_path = pathlib.Path(td) / f'{name}.iconset'
        iconset_path.mkdir()
        for size, scale in SIZES:
            resized = img.resize(
                size=(size*scale, size*scale), 
                resample=Image.BICUBIC,
            )
            scale_str = '' if scale == 1 else f'@{scale}x'
            resized_path = iconset_path / f'icon_{size}x{size}{scale_str}.png'
            resized.save(resized_path, format='PNG')
        coisos = (
            shutil.which('iconutil'),
            '-c',
            'icns',
            str(iconset_path),
            '-o',
            str(png_path.with_suffix('.icns')),
        )
        subprocess.run(coisos)


if __name__ == '__main__':

    try:
        png_path = pathlib.Path(sys.argv[1])
    except IndexError:
        sys.exit(f'usage: {sys.argv[0]} <png-image>')
    create_icns(png_path)

