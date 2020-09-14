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

        self.python_runtime_dir = None