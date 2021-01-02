"""
PUP Plugin implementing the 'win.create-msi' step.
"""

import logging
import os
import pathlib
import re
import shutil
import uuid
import zipfile

import cookiecutter
from cookiecutter import generate
try:
    # Python < 3.9
    import importlib_resources as ilr
except ImportError:
    import importlib.resources as ilr

from . import msi_wxs_template



_log = logging.getLogger(__name__)



class Step:

    """
    Extracts a `cookiecutter`-based Windows distribution template into the
    `build` directory (template variables are sourced from the context). Sets
    the context `python_runtime_dir`, pointing to where the Python runtime
    should be copied.
    """

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'win32') and
            (ctx.tgt_platform == 'win32')
        )

    def __call__(self, ctx, dsp):

        wix_root = self._ensure_wix(dsp)
        wix_src_path = self._create_wix_source(ctx, dsp)
        self._create_wix_manifest(ctx, dsp, wix_root, wix_src_path)
        self._compile_wix_sources(ctx, dsp, wix_root, wix_src_path)
        msi_file_path = self._link_wix_objects(ctx, dsp, wix_root, wix_src_path)

        ctx.final_artifact = msi_file_path
        _log.info('MSI file at %r.', str(msi_file_path))


    _WIX_BINARIES_URL = (
        'https://github.com/wixtoolset/wix3'
        '/releases/download/wix3112rtm/wix311-binaries.zip'
    )

    def _ensure_wix(self, dsp):

        wix_bin_zip = dsp.download(self._WIX_BINARIES_URL)
        wix_extract_dir = pathlib.Path(wix_bin_zip).with_suffix('.extracted')

        if wix_extract_dir.exists():
            return wix_extract_dir

        wix_extract_dir.mkdir()
        with zipfile.ZipFile(wix_bin_zip) as zf:
            zf.extractall(path=wix_extract_dir)

        return wix_extract_dir


    def _create_wix_source(self, ctx, dsp):

        tmpl_path = ilr.files(msi_wxs_template)
        tmpl_data = {
            'cookiecutter': {
                'app_name': ctx.nice_name,
                'version': ctx.src_metadata.version,
                'msi_version': self._msi_version(ctx.src_metadata.version),
                'author': ctx.src_metadata.author,
                'author_email': ctx.src_metadata.author_email,
                'url': ctx.src_metadata.home_page,
                'launch_module': self._launch_module_from_context(ctx),
                'guid': self._upgrade_code_guid(ctx),
            }
        }

        # "Generate + Remove + Generate" motivation: cookiecutter either fails
        # if the output path exists, or overwrites it. However, it does not
        # remove pre-existing files that are no longer templated. Thus, the
        # "proper" way to ensure output is consistent without deleting the
        # whole build directory is to "Generate + Remove + Generate again".

        build_dir = dsp.directories()['build']
        result_path = generate.generate_files(tmpl_path, tmpl_data, build_dir, overwrite_if_exists=True)
        shutil.rmtree(result_path, ignore_errors=True)
        result_path = generate.generate_files(tmpl_path, tmpl_data, build_dir)

        return pathlib.Path(result_path)


    # Copied from PEP 440
    _VERSION_PATTERN = r"""
        v?
        (?:
            (?:(?P<epoch>[0-9]+)!)?                           # epoch
            (?P<release>[0-9]+(?:\.[0-9]+)*)                  # release segment
            (?P<pre>                                          # pre-release
                [-_\.]?
                (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))
                [-_\.]?
                (?P<pre_n>[0-9]+)?
            )?
            (?P<post>                                         # post release
                (?:-(?P<post_n1>[0-9]+))
                |
                (?:
                    [-_\.]?
                    (?P<post_l>post|rev|r)
                    [-_\.]?
                    (?P<post_n2>[0-9]+)?
                )
            )?
            (?P<dev>                                          # dev release
                [-_\.]?
                (?P<dev_l>dev)
                [-_\.]?
                (?P<dev_n>[0-9]+)?
            )?
        )
        (?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?       # local version
    """

    _VERSION_RE = re.compile(
        r"^\s*" + _VERSION_PATTERN + r"\s*$",
        re.VERBOSE | re.IGNORECASE,
    )

    def _msi_version(self, version):

        # MSI versions are not as flexible as PEP 440's.
        # Let's adapt the version to three dot-separated numbers.

        result = self._VERSION_RE.match(version)
        pep440_release = result.group('release')

        numbers_only = pep440_release == version
        nums = pep440_release.split('.')
        num_count = len(nums)

        if num_count < 3:
            nums.extend(('0', '0'))

        msi_version = '.'.join(nums[:3])

        if not numbers_only or num_count != 3:
            _log.warning(
                'Version %r not MSI supported: using %r.',
                version,
                msi_version,
            )

        return msi_version


    def _launch_module_from_context(self, ctx):

        return ctx.launch_module if ctx.launch_module else ctx.src_metadata.name


    def _upgrade_code_guid(self, ctx):

        return str(uuid.uuid5(uuid.NAMESPACE_URL, ctx.src_metadata.home_page))


    def _create_wix_manifest(self, ctx, dsp, wix_root, wix_src_path):

        launch_module = self._launch_module_from_context(ctx)
        wix_manifest_path = wix_src_path / 'manifest.wxs'
        cmd = [
            str(wix_root / 'heat.exe'),
            'dir',
            str(ctx.relocatable_root),
            '-nologo',
            '-gg',
            '-sfrag',
            '-sreg',
            '-srd',
            '-scom',
            '-dr', f'{launch_module}_ROOTDIR',
            '-cg', f'{launch_module}_COMPONENTS',
            '-var', 'var.SourceDir',
            '-out', str(wix_manifest_path),
        ]

        dsp.spawn(
            cmd,
            out_callable=lambda line: _log.info('wix heat out: %s', line),
            err_callable=lambda line: _log.info('wix heat err: %s', line),
        )


    def _compile_wix_sources(self, ctx, dsp, wix_root, wix_src_path):

        # Must change CWD because candle.exe outputs to it. :/
        cwd = os.getcwd()
        try:
            os.chdir(str(wix_src_path))

            cmd = [
                str(wix_root / 'candle.exe'),
                '-nologo',
                f'-dSourceDir={ctx.relocatable_root}',
            ]
            cmd.extend(str(wxs_path) for wxs_path in pathlib.Path().glob('*.wxs'))

            dsp.spawn(
                cmd,
                out_callable=lambda line: _log.info('wix candle out: %s', line),
                err_callable=lambda line: _log.info('wix candle err: %s', line),
            )
        finally:
            os.chdir(cwd)


    def _link_wix_objects(self, ctx, dsp, wix_root, wix_src_path):

        dist_dir = dsp.directories()['dist']
        msi_file_path = dist_dir / self._msi_filename(ctx)

        cmd = [
            str(wix_root / 'light.exe'),
            '-nologo',
            '-spdb',
            '-o', str(msi_file_path),
        ]
        cmd.extend(str(wxs_path) for wxs_path in wix_src_path.glob('*.wixobj'))

        dsp.spawn(
            cmd,
            out_callable=lambda line: _log.info('wix light out: %s', line),
            err_callable=lambda line: _log.info('wix light err: %s', line),
        )

        return msi_file_path


    def _msi_filename(self, ctx):

        return f'{ctx.nice_name} {ctx.src_metadata.version}.msi'
