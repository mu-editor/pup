``pup`` | Pluggable Micro Packager
==================================

``pup`` is (in the early stages of becoming) a packaging tool for Python GUI programs.

Fundamentally,
its *raison d'être* is producing macOS and Windows native packages
for distributing the `Mu Editor <https://codewith.mu/>`_
to Python beginners around the world.
As a by-product of that,
it may very likely be effective at packaging
generic Python written GUI programs.
If that ever is the case,
then great.
Otherwise,
that's fine too.

The purpose,
again,
is to package `Mu Editor <https://codewith.mu/>`_
for macOS and Windows distribution.



Capabilities
------------

The current version of ``pup``,
while still very limited and somewhat exploratory,
can package,
at least,
the `Mu Editor <https://codewith.mu/>`_
and `puppy <https://github.com/tmontes/puppy/>`_ into distributable:

* **Windows MSI installer files**

  Minimally featured, user-installable,
  with an optional License Agreement GUI,
  adding an entry to the Windows Start Menu,
  with an optional custom icon.

  The packaged binary files can be signed,
  as well as the final MSI file.

  As a side-effect of the process,
  a relocatable directory holding the aplication is produced,
  paving the way for the creation "portable" Windows applications.

* **macOS DMG files**

  Holding the relocatable ``.app`` application bundle,
  with an optional custom icon,
  properly signed and notarized as required for distribution,

  Including an optional License Agreement GUI
  and custom volume icon.

* **Linux AppImage files**

  Preliminary support:
  limited to Python 3.8 on x86_64 systems,
  with the Desktop Entry's Categories hard-coded to "Education".


As of this writing,
``pup`` should be able to package any Python GUI application that:

* Runs on Python 3.7, on macOS or Windows.
* Runs on Python 3.8, on macOS, Linux or Windows.
* Is ``pip``-installable (no need to be on PyPI, though).
* Is launchable from the CLI with ``python -m <launch-module>``.

No specific efforts have been put forth to ensure that that is the case,
however,
so YMMV.



Installation
------------

``pup`` is distributed via `PyPI <https://pypi.org/pypi/pup>`_.
Install it with:

.. code-block:: console

	$ pip install pup



Generic Usage
-------------

To package an application, run:

.. code-block:: console

        $ pup package <pip-install-src>

Where:

* ``<pip-install-src>`` is the argument
  in the ``pip install <pip-install-src>`` command
  to install the application on the local Python environment.

  In general,
  if it's ``pip``-installable then it's probably ``pup``-packageable.


This usage pattern
assumes that the application GUI is launchable with ``python -m <name>``,
where ``<name>`` is extracted
from the metadata of a wheel created from ``<pip-install-src>``.
If that is not the case,
``pup`` can be told otherwise.
Read on.

When completed,
the final distributable artifact will be placed under ``./dist/``.


Packaging Options
~~~~~~~~~~~~~~~~~

* Use ``--launch-module=<name>``
  to set the module name
  that should be used to launch the application GUI,
  as with the ``python -m <name>`` command.

* Use ``--nice-name=<name>``
  to set a "nice name" for the application
  to be used used throughout the packaging process:
  in file and directory names,
  for macOS's application bundle and DMG file names,
  and for the Windows Start Menu entry.

  When omitted,
  that name is obtained from the metadata of a wheel
  created from ``<pip-install-src>``,
  that very often does not match the exact product spelling,
  as communicated to end-users.

* Use ``--icon-path=<icon-path>``
  to include a custom icon in the packaging process.

  On macOS the given file should be an
  `ICNS <https://en.wikipedia.org/wiki/Apple_Icon_Image_format>`_ file
  which will be used as the icon for both the packaged application bundle
  and the DMG file volume icon.

  On Linux the file should be a
  `PNG <https://en.wikipedia.org/wiki/Portable_Network_Graphics>`_ file
  which will be used as the icon for the running application.

  On Windows the file should be an
  `ICO <https://en.wikipedia.org/wiki/ICO_(file_format)>`_ file
  which will be used on the Windows Start Menu entry and
  on the Windows Programs and Features listing.

* Use ``--license-path=<license-path>`` to bundle the given license text
  and require users to accept it before installation
  (not currently supported on Linux AppImage).

  The given ``<license-path>`` must be an ASCII-encoded text file.

* Use ``--launch-pyflag=<flag>`` to override the default ``-I``
  `Python launch flag <https://docs.python.org/3/using/cmdline.html#cmdoption-I>`_
  (repeat for each flag to be used or set ``<flag>`` to the empty string to use none).


Signing
~~~~~~~

Signing is optional and varies slightly between platforms.

``pup`` will only sign the application for distribution
when all of the following conditions are true.
On macOS,
``pup`` will also complete the Apple required notarization process:
for that,
the packaging system must be online and
able to connect to Apple's notarization services
over the internet.

**macOS**

* XCode 10.3 or later must be installed
  -- the Command Line Tools are not enough.

* The following environment variables must be set:

  * ``PUP_SIGNING_IDENTITY``:
    10-digit identifier on the Apple Developer Certificate.
  * ``PUP_NOTARIZE_USER``:
    email address for the Apple Developer Account.
  * ``PUP_NOTARIZE_PASSWORD``:
    Application Specific Password.


**Windows**

* The Windows SDK must be installed,
  providing the ``signtool.exe`` utility.

* The following environment variable must be set:

  * ``PUP_SIGNING_IDENTITY``:
    *cname* of the code signing certificate.


Behaviour Notes
~~~~~~~~~~~~~~~
In the first run,
``pup`` downloads one or more files,
which are cached locally for later use:

* A relocatable Python Runtime from the
  `Python Build Standalone <https://python-build-standalone.readthedocs.io/>`_
  project.

* On Windows,
  the `WiX toolset <https://wixtoolset.org>`_,
  used to create MSI files.

``pup`` logs its progress to STDERR,
with fewer per-event details when it's a TTY.
The logging level defaults to ``INFO`` and can be changed
with either the ``--log-level`` CLI option,
or by setting the ``PUP_LOG_LEVEL`` environment variable.

Other than the locally cached files,
``pup`` creates files under:

* ``./build/pup/`` containing all intermediate artifacts..
* ``./dist/`` where the final distributable artifact is delivered..



-------------------------


Packaging the Mu Editor on Windows
----------------------------------

Requirements for signing:

* The Windows SDK must be installed.
* A code signing certificate must be available under Windows' *certmgr* utility.

Run:

.. code-block:: console

        > set PUP_SIGNING_IDENTITY=<signer>


Where:

* ``<signer>`` is the *cname* attribute of the code signing certificate.


Then, assuming the current working directory is Mu Editor's repository root, run:

.. code-block:: console

        > pup package
              --launch-module=mu
              --nice-name="Mu Editor"
              --icon-path=.\package\icons\win_icon.ico
              --license-path=.\LICENSE
              .

Note:

* The command is line-wrapped for readability, but must be input as a single line.
* One of the last packaging stages is signing.
* It will take a while as there are many files to be signed,
  but progress is continuously displayed,
  with the defaul log level.


Once completed:

* The resulting MSI file will be ``./dist/Mu Editor <version>.msi``.

* A by-product of that is the ``./build/pup/Mu Editor <version>/`` relocatable directory,
  containing a GUI-clickable script that launches Mu.
  Creating a ZIP file from it for distribution
  results in a minimally working "portable" Windows application.




Packaging the Mu Editor on macOS
--------------------------------

Requirements for signing and notarization:

* Must have XCode 10.3 or later installed.
* Must have an Apple Developer Certificate --
  see `this article's step 4
  <https://glyph.twistedmatrix.com/2018/01/shipping-pygame-mac-app.html>`_,
  for guidance.
* Must create an Application Specific Password --
  see `this article <https://support.apple.com/en-us/HT204397>`_,
  for guidance.

Run:

.. code-block:: console

        $ export PUP_SIGNING_IDENTITY=<signer>
        $ export PUP_NOTARIZE_USER=<user>
        $ export PUP_NOTARIZE_PASSWORD=<asp>

Where:

* ``<signer>`` is the 10-digit identifier on your Apple Developer Certificate's cname.
* ``<user>`` is the email address associated to you Apple Developer Account.
* ``<asp>`` is the Application Specific Password.


Then, assuming the current working directory is Mu Editor's repository root, run:

.. code-block:: console

        $ pup package \
              --launch-module=mu \
              --nice-name="Mu Editor" \
              --icon-path=./package/icons/mac_icon.icns \
              --license-path=./LICENSE \
              .

Note:

* One of the last packaging stages is notarization.
* It will take a while --
  no less than 3 minutes,
  IME,
  sometimes 10-15 minutes.
* The logged messages should help understand that the "thing" is not hung.
* Just be patient, I guess! :)


Once completed:

* The resulting DMG file will be ``./dist/<name> <version>.dmg``.

* A by-product of that is
  the ``./build/pup/Mu Editor.app/`` relocatable application bundle.
  Archiving it into a ZIP file, for distribution, should be perfectly fine.


More
----

To learn more about ``pup``
refer to the `online documentation <https://pup.readthedocs.io/>`_:
at this early stage,
it is mostly a collection
of thoughts and ideas
around behaviour,
requirements,
and very very rough internal design.

Development moves forward
on GitHub at https://github.com/mu-editor/pup/.


.. marker-end-welcome-dont-remove


Thanks
------

.. marker-start-thanks-dont-remove

- To Nicholas Tollervey, for the amazing `Mu Editor <https://codewith.mu/>`_.

- To the Mu Editor contributors
  I've been having the privilege of working more directly with,
  Carlos Pereira Atencio, Martin Dybdal, and Tim Golden, as well as the others
  whom I haven't met yet but whose contributions I highly respect.

- To Russell Keith-Magee, for the inspiring `BeeWare <https://beeware.org>`_ project
  and, in particular, for `briefcase <https://pypi.org/project/briefcase/>`_ that
  being used as the packaging tool for Mu on macOS as of this writing, serves as a
  great inspiration to ``pup``.

- To Gregory Szorc, for the incredible
  `Python Standalone Builds <https://python-build-standalone.readthedocs.io/>`_
  project,
  on top of which ``pup`` packages redistributable Python GUI applications.

- To Donald Stufft,
  for letting us pick up the ``pup`` name in `PyPI <https://pypi.org/project/pup/>`__.

- To Glyph Lefkowitz, for the very useful,
  high quality `Tips And Tricks for Shipping a PyGame App on the Mac
  <https://glyph.twistedmatrix.com/2018/01/shipping-pygame-mac-app.html>`_
  article,
  and for his generous hands-on involvement in the first-steps of ``pup``'s take
  on the subject `in this issue <https://github.com/mu-editor/pup/issues/43>`_.

- To Alastair Houghton, for `dmgbuild <https://pypi.org/project/dmgbuild/>`_,
  that ``pup`` uses to create macOS DMG files.

- To the `WiX Toolset <https://wixtoolset.org/>`__ developers, maintainers,
  contributors, and sponsors:
  not sure how ``pup`` would go about building Windows MSI installers without it.

.. marker-end-thanks-dont-remove



About
-----

.. marker-start-about-dont-remove

``pup`` is in the process of being created by Tiago Montes,
with the wonderful support of the Mu development team.

.. marker-end-about-dont-remove

