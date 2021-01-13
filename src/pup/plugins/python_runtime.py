"""
PUP Plugin implementing the 'pup.python-runtime' step.
"""

import json
import logging
import os
import pathlib
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

        url = os.environ.get(
            'PUP_PSB_URL',
            self._pbs_url(ctx.tgt_platform, ctx.tgt_python_version_suffix)
        )
        pbs_artifact = dsp.download(url)

        python_runtime_dir = ctx.python_runtime_dir
        runtime_parent_dir = python_runtime_dir.parent
        with tf.TemporaryDirectory(prefix='pup-', dir=runtime_parent_dir) as td:

            td = pathlib.Path(td)
            self._extract_zstd_file(pbs_artifact, td)

            pbs_py = td / 'python'
            pbs_py_json = self._load_pbs_python_json(pbs_py / 'PYTHON.json')

            pbs_py_paths = pbs_py_json['python_paths']
            pbs_data = pbs_py_paths['data']
            (pbs_py / pbs_data).replace(python_runtime_dir)

        # Track Python Runtime executable.
        ctx.python_rel_exe = self._relative(pbs_py_json['python_exe'], pbs_data)

        # Track Python Runtime paths than need cleaning up later.
        ctx.python_rel_scripts = self._relative(pbs_py_paths['scripts'], pbs_data)
        ctx.python_rel_stdlib = self._relative(pbs_py_paths['stdlib'], pbs_data)
        ctx.python_rel_site_packages = self._relative(pbs_py_paths['purelib'], pbs_data)

        ctx.python_test_packages = pbs_py_json['python_stdlib_test_packages']
        ctx.stdlib_platform_config = self._relative(
            pbs_py_json.get('python_stdlib_platform_config'),
            pbs_data,
        )
        


    def _relative(self, path, base):

        return pathlib.Path(path).relative_to(base) if path else None


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
