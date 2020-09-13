"""
PUP `build` and `dist` common directory definitions.
"""

import pathlib


DIRS = {
    'build': pathlib.Path('build') / 'pup',
    'dist': pathlib.Path('dist'),
}
