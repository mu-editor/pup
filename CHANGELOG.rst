Python Mu Packager Change Log
=============================

.. marker-start-of-change-log

.. towncrier release notes start

Pup 1.0.0a3 (2020-10-18)
------------------------

Enhancements
^^^^^^^^^^^^

- Resulting macOS application bundles are now signed and notarized.
  (`#43 <https://github.com/mu-editor/pup/issues/43>`_)
- Distributable artifacts now smaller.
  Many unneeded files and directory removed during the packaging process.
  (`#38 <https://github.com/mu-editor/pup/issues/38>`_)
- Subprocess output,
  like ``pip``'s,
  is now tracked and logged live.
  (`#32 <https://github.com/mu-editor/pup/issues/32>`_)

Bug Fixes
^^^^^^^^^

- macOS application bundles with names containing spaces now launch.
  (`#44 <https://github.com/mu-editor/pup/issues/44>`_)


Other Changes
^^^^^^^^^^^^^

- Renamed ``pup`` to *Pluggable Micro Packager*.
  (`#71 <https://github.com/mu-editor/pup/issues/71>`_)
- Added minimal usage documentation.
  (`#70 <https://github.com/mu-editor/pup/issues/70>`_)
- Updated development documentation.
  (`#68 <https://github.com/mu-editor/pup/issues/68>`_)
- Simpler log format when output is a TTY: no timestamps and no logger name.
  (`#52 <https://github.com/mu-editor/pup/issues/52>`_)
- Changed the default logging level to INFO.
  (`#58 <https://github.com/mu-editor/pup/issues/58>`_)
- Now logs exception tracebacks at CRITICAL level.
  (`#51 <https://github.com/mu-editor/pup/issues/51>`_)


Pup 1.0.0a2 (2020-09-16)
------------------------

- First release that actually does something.
  Minimal packaging to a relocatable directory works
  and includes a GUI clickable "thing" to launch the application --
  on macOS and Windows,
  for Python 3.7 and 3.8
  (`#34 <https://github.com/mu-editor/pup/issues/34>`_).



Pup 1.0.0a1 (2020-08-04)
------------------------

- ``pup`` exists as a CLI tool, is ``pip``-installable, and returns 42.

