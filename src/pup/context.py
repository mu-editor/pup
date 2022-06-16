"""
Packaging Context.
"""

import pathlib
from urllib import parse


class Context:

    def __init__(
        self,
        *,
        src,
        launch_module,
        launch_pyflags,
        nice_name,
        icon_path,
        license_path,
        ignore_plugins,
        platform,
        python_version,
    ):

        self.src = src
        self.launch_module = launch_module
        self.launch_pyflags = tuple(pyflag for pyflag in launch_pyflags if pyflag)
        self._nice_name = nice_name
        self.icon_path = pathlib.Path(icon_path).absolute() if icon_path else None
        self.license_path = pathlib.Path(license_path).absolute() if license_path else None

        if icon_path and not self.icon_path.exists():
            raise EnvironmentError(f'Non-existent icon path {icon_path!r}.')

        if license_path and not self.license_path.exists():
            raise EnvironmentError(f'Non-existent license path {license_path!r}.')

        self.src_wheel = None
        self.src_metadata = None

        self.ignore_plugins = ignore_plugins
        self.pkg_platform = platform
        self.tgt_platform = platform
        self.tgt_python_version = python_version

        self.relocatable_root = None

        self.python_runtime_dir = None
        self.python_rel_exe = None
        self.python_rel_scripts = None
        self.python_rel_stdlib = None
        self.python_rel_site_packages = None
        self.python_rel_tcl_library = None

        self.final_artifact = None


    @property
    def nice_name(self):
        """
        User facing packaged name.
        """
        return self._nice_name or self.src_metadata.name


    @property
    def application_id(self):
        """
        Returns the application identifier built from the package's home_page
        URL, consisting of two-sets of '.'-separated strings: the reverse DNS
        host/domain part, followed by the in-order path components.

        Example:
        - home_page='https://example.com/a/path'
        - bundle_id='com.example.a.path'
        """

        url_parts = parse.urlsplit(self.src_metadata.home_page)
        return '.'.join((
            '.'.join(reversed(url_parts.netloc.split('.'))),
            '.'.join(filter(None, url_parts.path.split('/')))
        ))
