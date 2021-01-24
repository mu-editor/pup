Python Mu Packager Change Log
=============================

.. marker-start-of-change-log

.. towncrier release notes start

Pup 1.0.0a8 (2021-01-24)
------------------------

Enhancements
^^^^^^^^^^^^

- The Python Build Standalone package to be used can now be overridden via the PUP_PBS_URL environment variable -- for now this is a stop gap capability to support packaging 32-bit Windows applications using, for example, `<https://github.com/indygreg/python-build-standalone/releases/download/20200822/cpython-3.7.9-i686-pc-windows-msvc-shared-pgo-20200823T0159.tar.zst>`_. (`#125 <https://github.com/mu-editor/pup/issues/125>`_)


Bug Fixes
^^^^^^^^^

- macOS packaged applications failed running ``tkinter`` and ``turtle`` code when such code was running under a virtual environment -- much like what Mu Editor does. Now fixed. (`#122 <https://github.com/mu-editor/pup/issues/122>`_)
- macOS DMG creation failed when ``pup`` was installed into a virtual environment but invoked without activating it. Now fixed. (`#125 <https://github.com/mu-editor/pup/issues/125>`_)


Other Changes
^^^^^^^^^^^^^

- Changed the packaging sequence. (`#128 <https://github.com/mu-editor/pup/issues/128>`_)


Pup 1.0.0a7 (2021-01-10)
------------------------

Bug Fixes
^^^^^^^^^

- PyPI distributed ``pup`` failed miserably because it did not include all of its own bundled templates -- now fixed. (`#118 <https://github.com/mu-editor/pup/issues/118>`_)


Pup 1.0.0a6 (2021-01-06)
------------------------

Enhancements
^^^^^^^^^^^^

- The new ``--nice-name`` packaging option overrides the default application name,
  extracted from the distribution's metadata,
  with a more user-friendly name. (`#41 <https://github.com/mu-editor/pup/issues/41>`_)
- The packaging process can now use custom icons via the ``--icon-path`` option.
  Custom icons are used on macOS application bundles and DMG files,
  as well as on the Windows Start Menu and *Program and Features* entries. (`#90 <https://github.com/mu-editor/pup/issues/90>`_)
- An optional license agreement can now be provided with the ``--license-path`` option.
  It must be an ASCII-encoded text file that will be displayed to end-users,
  requiring their agreement before the installation can proceed. (`#91 <https://github.com/mu-editor/pup/issues/91>`_)
- The Windows packaging process
  can now sign the packaged binary ``.exe.``, ``.dll``, and ``.pyd`` files,
  as well as the final MSI file. (`#97 <https://github.com/mu-editor/pup/issues/97>`_)
- Updated the documentation and added a few entries to the "thanks" list. (`#108 <https://github.com/mu-editor/pup/issues/108>`_)


Bug Fixes
^^^^^^^^^

- Fixed a bug that prevented packaging non-signed Windows applications. (`#101 <https://github.com/mu-editor/pup/issues/101>`_)
- Fixed a bug that prevented macOS signing and notarization with the ``--nice-name`` option. (`#111 <https://github.com/mu-editor/pup/issues/111>`_)


Other Changes
^^^^^^^^^^^^^

- Updated versions of direct dependencies. (`#109 <https://github.com/mu-editor/pup/issues/109>`_)


Pup 1.0.0a5 (2020-12-08)
------------------------

Enhancements
^^^^^^^^^^^^

- Minmally usable macOS DMG files are now produced:
  no icons,
  no customization yet. (`#66 <https://github.com/mu-editor/pup/issues/66>`_)
- Minimally usable Windows MSI files are now produced.
  They are user-installable,
  do not include a GUI,
  and add a single Start Menu entry,
  for now,
  with no custom icon.
  Its implementation depends on the `WiX toolset <https://wixtoolset.org>`_,
  which is automatically downloaded and cached for subsequent usage. (`#82 <https://github.com/mu-editor/pup/issues/82>`_)
- Updated the documentation to reflect the new capabilities. (`#94 <https://github.com/mu-editor/pup/issues/94>`_)


Bug Fixes
^^^^^^^^^

- Running the Windows ``.vbs`` launcher from a directory other than the one containing it,
  in a CLI,
  no longer fails. (`#48 <https://github.com/mu-editor/pup/issues/48>`_)


Other Changes
^^^^^^^^^^^^^

- Updated PyPI classifiers: no longer planning but in alpha.
  For now we only support Python 3.7 and 3.8. (`#81 <https://github.com/mu-editor/pup/issues/81>`_)
- Some third party direct dependency versions were updated. (`#89 <https://github.com/mu-editor/pup/issues/89>`_)


Pup 1.0.0a4 (2020-11-18)
------------------------

Bug Fixes
^^^^^^^^^

- Fixed `pup` packaging so that the required cookiecutter templates are bundled. (`#77 <https://github.com/mu-editor/pup/issues/77>`_)


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

