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
        pip_platform,
        python_version,
    ):

        self.src = src
        self.launch_module = launch_module
        self.launch_pyflags = tuple(pyflag for pyflag in launch_pyflags if pyflag)
        self.given_nice_name = nice_name

        self._icon_path = None
        self.icon_path = pathlib.Path(icon_path).absolute() if icon_path else None

        self._license_path = None
        self.license_path = pathlib.Path(license_path).absolute() if license_path else None

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

        self.pip_platform = pip_platform


    @property
    def nice_name(self):
        """
        User facing packaged name.
        """
        return self.given_nice_name or self.src_metadata.name


    @property
    def icon_path(self):
        """
        Path to the packaged application Icon.
        """
        return self._icon_path


    @icon_path.setter
    def icon_path(self, value):

        if value and not value.exists():
            raise EnvironmentError(f'Non-existent icon path {str(value)!r}.')
        self._icon_path = value


    @property
    def license_path(self):
        """
        Path to the license text file.
        """
        return self._license_path

    @license_path.setter
    def license_path(self, value):

        if value and not value.exists():
            raise EnvironmentError(f'Non-existent license path {str(value)!r}.')
        self._license_path = value


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
