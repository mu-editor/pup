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
        appimage_tool = self._ensure_appimage_tool(dsp)

        cwd = os.getcwd()
        try:
            os.chdir(dist_dir)
            cmd = [
                str(appimage_tool),
                appdir_src,
            ]
            dsp.spawn(
                cmd,
                out_callable=lambda line: _log.info('appimagetool out: %s', line),
                err_callable=lambda line: _log.info('appimagetool err: %s', line),
            )
        finally:
            os.chdir(cwd)


    _APPIMAGE_TOOL_URL =(
        'https://github.com/AppImage/AppImageKit/'
        '/releases/download/13/appimagetool-x86_64.AppImage'
    )

    def _ensure_appimage_tool(self, dsp):

        appimage_tool = dsp.download(self._APPIMAGE_TOOL_URL)
        appimage_tool.chmod(0o555)
        return appimage_tool
