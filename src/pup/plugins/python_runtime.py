"""
PUP Plugin implementing the 'pup.python-runtime' step.
"""

import json
import logging
import pathlib
import shutil
import tarfile
import tempfile as tf

import zstandard


_log = logging.getLogger(__name__)



_PYTHON_BUILD_STANDALONE_URLs = {
    'darwin': {
        '3.7': 'https://github.com/indygreg/python-build-standalone/releases/download/20200823/cpython-3.7.9-x86_64-apple-darwin-pgo-20200823T2228.tar.zst',
        '3.8': 'https://github.com/indygreg/python-build-standalone/releases/download/20200823/cpython-3.8.5-x86_64-apple-darwin-pgo-20200823T2228.tar.zst',
    },
    'win32': {
        '3.7': 'https://github.com/indygreg/python-build-standalone/releases/download/20200822/cpython-3.7.9-x86_64-pc-windows-msvc-shared-pgo-20200823T0118.tar.zst',
        '3.8': 'https://github.com/indygreg/python-build-standalone/releases/download/20200830/cpython-3.8.5-x86_64-pc-windows-msvc-shared-pgo-20200830T2254.tar.zst',
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

        url = self._pbs_url(ctx.tgt_platform, ctx.tgt_python_version_suffix)

        pbs_artifact = dsp.download(url)

        runtime_parent_dir = ctx.python_runtime_dir.parent
        with tf.TemporaryDirectory(prefix='pup-', dir=runtime_parent_dir) as td:

            td = pathlib.Path(td)
            self._extract_zstd_file(pbs_artifact, td)

            pbs_python = td / 'python'
            pbs_python_json = self._load_pbs_python_json(pbs_python / 'PYTHON.json')

            pbs_data = pbs_python_json['python_paths']['data']
            (pbs_python / pbs_data).replace(ctx.python_runtime_dir)

        pbs_python_exe = pathlib.Path(pbs_python_json['python_exe'])
        relative_python_exe = pbs_python_exe.relative_to(pbs_data)
        ctx.python_runtime_exec = ctx.python_runtime_dir / relative_python_exe


    def _pbs_url(self, platform, py_version):

        try:
            return _PYTHON_BUILD_STANDALONE_URLs[platform][py_version]
        except KeyError:
            raise RuntimeError(f'No {platform} Python runtime for Python {py_version}.')


    def _extract_zstd_file(self, filename, target_dir):

        with open(filename, 'rb') as input_file:
            decompressor = zstandard.ZstdDecompressor()
            with decompressor.stream_reader(input_file) as reader:
                with tarfile.open(mode='r|', fileobj=reader) as tf:
                    tf.extractall(path=target_dir)


    def _load_pbs_python_json(self, filename):

        with open(filename, 'rt', encoding='utf8') as input_file:
            return json.load(input_file)
