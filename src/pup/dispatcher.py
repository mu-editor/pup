"""
Tracks available plugins.
"""

import logging

try:
    import importlib.metadata as ilm
except ImportError:
    # Python <= 3.8
    import importlib_metadata as ilm



_log = logging.getLogger(__name__)



class Dispatcher:

    def __init__(self, ctx):

        all_plugin_entry_points = ilm.entry_points().get('pup.plugins', ())
        self._plugin_entry_points = [
            entry_point
            for entry_point in all_plugin_entry_points
            if not self._ignore(entry_point, ctx.ignore_plugins)
        ]
        _log.debug('plugin_entry_points=%r', self._plugin_entry_points)


    @staticmethod
    def _ignore(entry_point, ignore_plugins):

        return any(
            entry_point.value.startswith(ignore_plugin)
            for ignore_plugin in ignore_plugins
        )


    def _classes_and_names_for(self, what):
        return [
            (entry_point.load(), entry_point.value)
            for entry_point in self._plugin_entry_points
            if entry_point.name.startswith(f'{what}.')
        ]


    @staticmethod
    def _class_names(classes):
        return [repr(f'{cls.__module__}.{cls.__name__}') for cls in classes]


    def stages(self, ctx):
        classes_and_names = [
            (plugin_class, name)
            for plugin_class, name in self._classes_and_names_for('stages')
            if plugin_class.usable_in(ctx)
        ]
        count = len(classes_and_names)
        if count != 1:
            names = ', '.join(repr(name) for _, name in classes_and_names)
            raise RuntimeError(f'{count} packaging stage plugins: {names}.')

        plugin_class, _ = classes_and_names[0]
        plugin = plugin_class()
        return plugin(ctx)
