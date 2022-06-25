import logging
import os



_log = logging.getLogger(__name__)



class Step:

    @staticmethod
    def usable_in(ctx):
        return (
            (ctx.pkg_platform == 'linux') and
            (ctx.tgt_platform == 'linux')
        )

    def __call__(self, ctx, dsp):

        build_dir = dsp.directories()['build']
        build_dir.mkdir(parents=True, exist_ok=True)
        dist_dir = dsp.directories()['dist']
        dist_dir.mkdir(parents=True, exist_ok=True)

        appdir_src = (build_dir / f'{ctx.nice_name}.AppDir').absolute()
        appimage_tool = self._ensure_appimage_tool(dsp, build_dir)

        cwd = os.getcwd()
        try:
            os.chdir(dist_dir)
            env = dict(os.environ)
            env['VERSION'] = ctx.src_metadata.version
            cmd = [
                str(appimage_tool),
                appdir_src,
            ]
            dsp.spawn(
                cmd,
                out_callable=lambda line: _log.info('appimagetool out: %s', line),
                err_callable=lambda line: _log.info('appimagetool err: %s', line),
                env=env,
            )
        finally:
            os.chdir(cwd)


    _APPIMAGE_TOOL_URL = os.environ.get(
        'PUP_AIT_URL',
        'https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage',
    )

    def _ensure_appimage_tool(self, dsp, build_dir):

        appimage_tool = dsp.download(self._APPIMAGE_TOOL_URL)
        appimage_tool.chmod(0o555)

        # The downloaded tool is itself an AppImage that fails to run under
        # Docker containers. Workaround: extract the AppImage and return the
        # embedded command/entrypoint.

        appimage_tool_dir = build_dir / 'appimagetool'
        appimage_tool_dir.mkdir(parents=True, exist_ok=True)

        cwd = os.getcwd()
        try:
            os.chdir(appimage_tool_dir)
            cmd = [
                str(appimage_tool),
                '--appimage-extract',
            ]
            dsp.spawn(
                cmd,
                out_callable=lambda line: _log.info('appimagetool out: %s', line),
                err_callable=lambda line: _log.info('appimagetool err: %s', line),
            )
        finally:
            os.chdir(cwd)

        # The embedded entry point:
        appimage_tool = appimage_tool_dir / 'squashfs-root' / 'AppRun'

        return appimage_tool.absolute()
