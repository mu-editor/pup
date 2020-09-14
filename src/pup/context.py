"""
Packaging Context.
"""

class Context:

    def __init__(self, *, src, ignore_plugins, platform, python_version):

        self.src = src
        self.src_metadata = None

        self.ignore_plugins = ignore_plugins
        self.pkg_platform = platform
        self.tgt_platform = platform
        self.tgt_python_version = python_version[:3]
        self.tgt_python_version_suffix = '.'.join(map(str, python_version[:2]))

        self.python_runtime_dir = None
        self.python_runtime_exec = None
