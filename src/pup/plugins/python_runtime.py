"""
PUP Plugin implementing the 'pup.python-runtime' step.
"""

import logging
import shutil
import tarfile

import zstandard


_log = logging.getLogger(__name__)



_PYTHON_BUILD_STANDALONE_URLs = {
    'darwin': {
        (3, 7): 'https://github.com/indygreg/python-build-standalone/releases/download/20200823/cpython-3.7.9-x86_64-apple-darwin-pgo-20200823T2228.tar.zst',
        (3, 8): 'https://github.com/indygreg/python-build-standalone/releases/download/20200823/cpython-3.8.5-x86_64-apple-darwin-pgo-20200823T2228.tar.zst',
    },
    'win32': {
        (3, 7): 'https://github.com/indygreg/python-build-standalone/releases/download/20200822/cpython-3.7.9-x86_64-pc-windows-msvc-shared-pgo-20200823T0118.tar.zst',
        (3, 8): 'https://github.com/indygreg/python-build-standalone/releases/download/20200830/cpython-3.8.5-x86_64-pc-windows-msvc-shared-pgo-20200830T2254.tar.zst',
    },
}



class Step:

    """
    Downloads and extracts a relocatable Python runtime for the target platform
    into the directory specified by the context.
    """

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'darwin') or
            (ctx.pkg_platform == 'win32')
        ) and (
            (ctx.pkg_platform == ctx.tgt_platform)
        )

    def __call__(self, ctx, dsp):

        platform = ctx.tgt_platform
        py_version = ctx.tgt_python_version[:2]

        try:
            url = _PYTHON_BUILD_STANDALONE_URLs[platform][py_version]
        except KeyError:
            raise RuntimeError(f'No {platform} Python runtime for Python {py_version}.')

        pbs_download = dsp.download(url)

        extract_dir = ctx.python_runtime_dir
        with open(pbs_download, 'rb') as input_file:
            decompressor = zstandard.ZstdDecompressor()
            with decompressor.stream_reader(input_file) as reader:
                with tarfile.open(mode='r|', fileobj=reader) as tf:
                    tf.extractall(path=extract_dir)

        # Adjust the layout and remove uneeded things
        for dirname in ('bin', 'lib', 'share'):
            source = extract_dir / 'python/install' / dirname
            shutil.move(str(source), str(extract_dir))
        shutil.rmtree(extract_dir / 'python')

        # Size optimization
        delete_these = [
            'lib/python3.7/config-3.7m-darwin',
            'lib/python3.7/test',
        ]
        for this in delete_these:
            shutil.rmtree(extract_dir / this)
