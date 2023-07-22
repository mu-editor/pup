"""
PUP Plugin implementing the 'pup.pip-install' step.
"""

import logging
import subprocess
import os


_log = logging.getLogger(__name__)



class Step:

    """
    Downloads 
    """

    @staticmethod
    def usable_in(ctx):
        return (
            ctx.pkg_platform in ('darwin', 'win32', 'linux')
        ) and (
            (ctx.pkg_platform == ctx.tgt_platform)
        )

    def __call__(self, ctx, dsp):
        python_path = str(ctx.python_runtime_dir / ctx.python_rel_exe)

        platform_flags = []
        if ctx.pip_platform:
            platform_flags.append('--platform={}'.format(ctx.pip_platform))
            platform_flags.append('--only-binary=:all:')
            # TODO: This should probably be done with the spawn helpers, but
            #       done this way as a proof of concept
            site_packages_path = subprocess.check_output([
                python_path,
                '-c',
                'import site; print(site.getsitepackages()[0], end="")'
            ])
            site_packages_path = site_packages_path.decode("utf-8")
            if os.path.isdir(site_packages_path):
                platform_flags.append('--target')
                platform_flags.append('{}'.format(site_packages_path))
            else:
                raise Exception("Invalid site-packages directory: {}".format(site_packages_path))

        cmd = [
            python_path,
            '-m',
            'pip',
            'install',
            '--no-warn-script-location',
            *platform_flags,
            ctx.src_wheel,
        ]

        _log.info('About to run %r.', ' '.join(cmd))

        dsp.spawn(
            cmd,
            out_callable=lambda line: _log.info('pip out: %s', line),
            err_callable=lambda line: _log.info('pip err: %s', line),
        )
