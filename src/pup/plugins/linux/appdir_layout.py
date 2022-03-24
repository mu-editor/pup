import logging
import pathlib
import shutil

import cookiecutter
from cookiecutter import generate
try:
    # Python < 3.9
    import importlib_resources as ilr
except ImportError:
    import importlib.resources as ilr

from . import appdir_template


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

        tmpl_path = ilr.files(appdir_template)
        tmpl_data = {
            'cookiecutter': {
                'nice_name': ctx.nice_name,
                'launch_module': self._launch_module_from_context(ctx),
                'launch_pyflags': ' '.join(ctx.launch_pyflags),
                'python_exe': ctx.python_rel_exe.name,
                'tcl_library': ctx.python_rel_tcl_library,
                'categories': 'Education',
            }
        }

        result_path = generate.generate_files(tmpl_path, tmpl_data, build_dir, overwrite_if_exists=True)
        shutil.rmtree(result_path, ignore_errors=True)
        result_path = generate.generate_files(tmpl_path, tmpl_data, build_dir)

        # Copy any given icon file into the bundle.
        if ctx.icon_path:
            shutil.copyfile(
                ctx.icon_path,
                pathlib.Path(result_path) / f'{ctx.nice_name}.png',
            )
        # Ensure AppRun is executable.
        (pathlib.Path(result_path) / 'AppRun').chmod(0o555)

        # Remove the .gitignore file in template (keeps empty dir in git).
        (pathlib.Path(result_path) / 'usr/.gitignore').unlink()

        new_python_runtime_dir = pathlib.Path(result_path) / 'usr'
        ctx.python_runtime_dir.replace(new_python_runtime_dir)
        ctx.python_runtime_dir = new_python_runtime_dir



    def _launch_module_from_context(self, ctx):

        return ctx.launch_module if ctx.launch_module else ctx.src_metadata.name
