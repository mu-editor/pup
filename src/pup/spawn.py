"""
Spawning child processes while tracking their output.
"""

import logging
import subprocess
import threading


_log = logging.getLogger(__name__)



def _copy_lines(readable, write_callable):

    for line in iter(readable.readline, ''):
        write_callable(line.rstrip('\n'))



def spawn(command, out_callable=None, err_callable=None, encoding='utf8'):
    """
    Spawns a child process specified by `command` which is passed to
    subprocess.Popen where `out/err_callable` is called for each stdout/err
    line that the child process produces, assumed to be text in the given
    `encoding`.
    """

    _log.debug('Spawning %r.', command)
    child = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0,
        encoding=encoding,
        universal_newlines=True,
    )
    _log.debug('Spawned PID %s.', child.pid)

    # Let's have callables to ensure we consume the child's out/err streams.
    out_callable = out_callable if out_callable else lambda line: None
    err_callable = err_callable if err_callable else lambda line: None

    # Spawn one thread per stream to drive the child to callable I/O.
    out_thread = threading.Thread(target=_copy_lines, args=(child.stdout, out_callable))
    err_thread = threading.Thread(target=_copy_lines, args=(child.stderr, err_callable))
    out_thread.start()
    err_thread.start()

    child_exit_status = child.wait()

    out_thread.join()
    err_thread.join()

    _log.debug('Child terminated with exit status %s', child_exit_status)
    return child_exit_status
