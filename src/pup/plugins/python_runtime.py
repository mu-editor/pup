"""
PUP Plugin implementing the 'pup.python-runtime' step.
"""

import json
import logging
import os
import pathlib
import shutil
import tarfile
import tempfile as tf

import zstandard


_log = logging.getLogger(__name__)



_PYTHON_BUILD_STANDALONE_URLs = {
    'darwin': {
        '3.7': 'https://github.com/indygreg/python-build-standalone/releases/download/20200823/cpython-3.7.9-x86_64-apple-darwin-pgo-20200823T2228.tar.zst',
        '3.8': 'https://github.com/indygreg/python-build-standalone/releases/download/20210724/cpython-3.8.11-x86_64-apple-darwin-pgo-20210724T1424.tar.zst',
    },
    'win32': {
        '3.7': 'https://github.com/indygreg/python-build-standalone/releases/download/20200822/cpython-3.7.9-x86_64-pc-windows-msvc-shared-pgo-20200823T0118.tar.zst',
        '3.8': 'https://github.com/indygreg/python-build-standalone/releases/download/20210724/cpython-3.8.11-x86_64-pc-windows-msvc-shared-pgo-20210724T1424.tar.zst',
    },
    'linux': {
        '3.8': 'https://github.com/indygreg/python-build-standalone/releases/download/20211012/cpython-3.8.12-x86_64-unknown-linux-gnu-pgo-20211011T1926.tar.zst',
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

        build_dir = self._ensure_build_dir(dsp)
        pbs_dir = build_dir / 'pbs'

        pbs_artifact = self._get_pbs_artifact(ctx, dsp)
        self._extract_zstd_file(pbs_artifact, pbs_dir)

        pbs_py_dir = pbs_dir / 'python'
        pbs_py_json = self._load_pbs_python_json(pbs_py_dir / 'PYTHON.json')

        pbs_py_paths = pbs_py_json['python_paths']
        pbs_data = pbs_py_paths['data']

        # Delete unneeded things.
        self._delete_test_packages(pbs_py_dir, pbs_py_json)
        self._delete_platform_config(pbs_py_dir, pbs_py_json)

        # Track key Python Runtime paths.
        ctx.python_runtime_dir = pbs_py_dir / pbs_data
        ctx.python_rel_exe = self._relative(pbs_py_json['python_exe'], pbs_data)
        ctx.python_rel_scripts = self._relative(pbs_py_paths['scripts'], pbs_data)
        ctx.python_rel_stdlib = self._relative(pbs_py_paths['stdlib'], pbs_data)
        ctx.python_rel_site_packages = self._relative(pbs_py_paths['purelib'], pbs_data)

        # Find `init.tcl` path (macOS needs the TCL_LIBRARY env var set).
        tcl_library_path = pbs_py_dir / pbs_py_json['tcl_library_path']
        init_tcl_path = None
        for candidate_path in pbs_py_json['tcl_library_paths']:
            init_tcl_path = tcl_library_path / candidate_path / 'init.tcl'
            if init_tcl_path.exists():
                break
        ctx.python_rel_tcl_library = self._relative(
            self._relative(init_tcl_path.parent, pbs_py_dir),
            pbs_data,
        )


    def _ensure_build_dir(self, dsp):

        build_dir = dsp.directories()['build']
        build_dir.mkdir(parents=True, exist_ok=True)
        return build_dir


    def _get_pbs_artifact(self, ctx, dsp):

        url = os.environ.get(
            'PUP_PBS_URL',
            self._pbs_url(ctx.tgt_platform, ctx.tgt_python_version_suffix)
        )
        return dsp.download(url)


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

    def _delete_tree(self, path):

        delete = str(path)
        _log.debug('Deleting %r...', delete)
        shutil.rmtree(delete, ignore_errors=True)


    def _delete_test_packages(self, pbs_py_dir, pbs_py_json):

        _log.info('Deleting Standard Library test packages...')
        stdlib_path = pbs_py_json['python_paths']['stdlib']
        for test_package in pbs_py_json['python_stdlib_test_packages']:
            test_package_path = test_package.replace('.', '/')
            self._delete_tree(pbs_py_dir / stdlib_path / test_package_path)


    def _delete_platform_config(self, pbs_py_dir, pbs_py_json):

        _log.info('Deleting Platform Config files...')
        stdlib_platform_config = pbs_py_json.get('python_stdlib_platform_config')
        if not stdlib_platform_config:
            return
        self._delete_tree(pbs_py_dir / stdlib_platform_config)


    def _relative(self, path, base):

        return pathlib.Path(path).relative_to(base) if path else None
