"""
Common functions for cross-platform plugins.
"""

def log_lines(log_callable, marker, lines):

    log_callable('%s start', marker)
    for line in lines.splitlines():
        log_callable('%s', line)
    log_callable('%s done', marker)
