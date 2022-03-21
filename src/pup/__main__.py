"""
Command line interface for PUP.
"""

import functools
import logging
import os
import sys

import click

from . import __title__ as sw_title, __version__ as sw_version
from . import api
from . import logs



_log = logging.getLogger(__package__)



def command_wrapper(command_function):
    """
    Decorator for click.command functions that i) logs version at start/finish,
    ii) logs exceptions raised during execution, iii) sets process exit status.
    """
    @functools.wraps(command_function)
    def wrapper(*args, **kw):
        _log.info('%s %s - starting with PID=%r', sw_title, sw_version, os.getpid())
        try:
            exit_code = command_function(*args, **kw)
        except Exception as exc:
            _log.critical('Execution failure: %s', exc)
            _log.critical('Traceback below:', exc_info=exc)
            exit_code = -1
        except BaseException:
            # KeyboardInterrupt exceptions (CTRL-C, SIGINT)
            exit_code = -2
        finally:
            _log.info('%s %s - done', sw_title, sw_version)
            sys.exit(exit_code)

    return wrapper




@click.group()
@click.version_option(version=sw_version)
@click.option(
    '--log-level',
    type=click.Choice(
        ['CRITICAL', 'ERROR', 'WARNING', 'WARN', 'INFO', 'DEBUG'],
        case_sensitive=False,
    ),
    default='INFO',
    show_default=True,
    envvar='PUP_LOG_LEVEL',
)
def main(log_level):
    """
    Pluggable Micro Packager.
    """
    logs.start(log_level)



@main.command()
@click.option('--ignore-plugin', 'ignore_plugins', multiple=True)
@click.option('--launch-module')
@click.option('--launch-pyflag', 'launch_pyflags', multiple=True, default=['-I',])
@click.option('--nice-name')
@click.option('--icon-path')
@click.option('--license-path')
@click.argument('src')
@command_wrapper
def package(src, ignore_plugins, launch_module, launch_pyflags, nice_name, icon_path, license_path):
    """
    Packages the GUI application in the given pip-installable source.
    """
    return api.package(
        src,
        ignore_plugins=ignore_plugins,
        launch_module=launch_module,
        launch_pyflags=launch_pyflags,
        nice_name=nice_name,
        icon_path=icon_path,
        license_path=license_path,
    )
