import pathlib
import sys

from PIL import Image

SIZES = [
    (16, 16),
    (24, 24),
    (32, 32),
    (48, 48),
    (64, 64),
    (128, 128),
    (256, 256),
]

def create_ico(png_path):

    img = Image.open(png_path)
    img.save(
        png_path.with_suffix('.ico'),
        format='ICO',
        sizes=SIZES,
    )


if __name__ == '__main__':

    try:
        png_path = pathlib.Path(sys.argv[1])
    except IndexError:
        sys.exit(f'usage: {sys.argv[0]} <png-image>')
    create_ico(png_path)


