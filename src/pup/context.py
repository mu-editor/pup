"""
Packaging Context.
"""

class Context:

    def __init__(self, *, ignore_plugins, platform, python_version, ):

        self.ignore_plugins = ignore_plugins
        self.pkg_platform = platform
        self.tgt_platform = platform
        self.tgt_python_version = python_version[:3]
