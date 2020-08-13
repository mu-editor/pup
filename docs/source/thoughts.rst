Thoughts
========

.. note::

   This is a draft of an *in progress* section, as of now.
   You have been warned! :)



Preliminary words on how ``pup`` could work that should help:

* Determine usage patterns.

* Define fundamental concepts.

* Identify challenges and requirements.



Packaging a Python GUI Application
----------------------------------

*...aka, the famous last "how hard can it be?" words.*

A possible way to package a Python GUI application is as follows:

1. Lay a relocatable Python distribution in a newly created *build* directory.

2. Use that Python distribution's ``pip`` to install the application.

3. Create an GUI level *thing* such that (double)-clicking it launches the application.

4. Package the whole thing in a single distributable and installable file.


Easy, see? :)

We might even add another step that distributes the packaged application
to the *application stores* of the world...
But let's not get ahead of ourselves
and dig a bit deeper, instead.
Of course the devil will be in the details --
let's see...



Really Packaging a Python GUI Application
-----------------------------------------

Stage 1 | Works from the CLI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Lay a relocatable Python distribution in a *build* directory.

   Candidates:

   * Gregory Szorc's
     `Python Standalone Builds <https://python-build-standalone.readthedocs.io/>`_.
     Preliminary ad-hoc testing showed it to work nicely
     on both macOS and Windows --
     should work on Linux, too.

   * The Python environment that's running ``pup`` itself.
     Would avoid an external dependency (and download!).
     Maybe making it relocatable is non trivial.
     Not sure if it could be distributed, license-wise.

   Needs thinking:

   * How will we know where to get a Python Standalone Build from?
   * We should (optionally?) cache such downloads.

2. Use that Python distribution's ``pip`` to install the application.
   By definition,
   it will be installed within that environment's ``site-packages``,
   along with its dependencies.

   Implies:

   * Packaging for the same platform we're running on.
     Otherwise, that Python distribution wouldn't be executable locally.
     More, maybe ``pip`` does not install non-native binary wheels from PyPI:
     Windows PyQt5, while packaging on macOS?
   * The application must be ``pip install``-able,
   * ...declare one `setuptools <https://setuptools.readthedocs.io/>`_
     `entry point <https://setuptools.readthedocs.io/en/latest/pkg_resources.html#entry-points>`_,
   * ...and/or is runnable with ``python -m <application.``.

At this point,
the application should be launchable from a CLI,
by either running the ``pip install``-ed entry point executable
or ``python -m <application>``
within the relocatable Python environment.


Stage 2 | Works from the GUI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On macOS:

1. Create a bare-bones `application bundle <https://developer.apple.com/library/archive/documentation/CoreFoundation/Conceptual/CFBundles/BundleTypes/BundleTypes.html>`_,
   maybe off of a template.

   Application bundles are directories
   containing a set of predefined files and sub-directories,
   holding everything needed to run the application:
   executable, libraries, resources, etc.
   For end users,
   application bundles look like files in the Finder.

   Thoughts:

   * Maybe `cookiecutter <https://pypi.org/project/cookiecutter/>`_ can be of use.
   * Such template could be somehow bundled, with no need for downloads.
     Overriding it should be possible, though.

2. Copy the relocatable Python distribution
   from Stage 1
   into the application bundle.

   No thoughts,
   should be trivial:
   `shutil <https://docs.python.org/3/library/shutil.html>`_ is our friend.

3. Create the application bundle's executable,
   under the ``MacOS`` sub-directory,
   as a shell-script that runs the application's entry point executable.

   Thoughts:

   * Care must be taken to avoid having absolute paths,
     which the application's entry point executable probably includes.
   * Maybe the templated application bundle can include this from the start.

At this point,
the application should be launchable from the Finder.


On Windows:

1. Create an appliction directory layout,
   somewhat inspired on macOS's application bundles.

   Thoughts:

   * Let's use the same templated solution as for macOS, if any.

2. Copy the relocatable Python distribution
   from Stage 1
   into it.

3. Create the application's *explorer clickable thing* as a
   `shell link <https://docs.microsoft.com/en-us/windows/win32/shell/links>`_
   in the root of the application directory layout.

   Thoughts:

   * It should either run the application's entry point executable or
     the relocatable ``python`` binary with a ``-m <application>`` argument.
     Either of these options still needs evaluation:
     on one hand,
     we're not sure yet if the application's entry point executable is relocatable
     (thus failing to run when the whole application directory is moved);
     on the other,
     going ``python -m <application>`` imposes further requirements on the way
     the application is created.
   * All in all, this step may not be strictly needed,
     given that on a later stage everything will be bundled into an installable file
     that itself will be responsible for creating a *Start Menu* link,
     much like this one.

   How to do this:

   * Use `winshell <https://pypi.org/project/winshell/>`_ by none other
     than Tim Golden, a Mu contributor. :)
   * Maybe get some ideas from
     `this stack overflow link <https://stackoverflow.com/questions/30028709/how-do-i-create-a-shortcut-via-command-line-in-windows>`_.

On Linux:

1. *[TBD]*

2. ...

3. *[profit?!]* :)


Stage 3 | Create a distributable artifact
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On macOS:

There are two common ways of distributing applications:
via DMG (disk image) or PKG (packaged installer) files.
The former tends to be simpler
and that's what we'll be initially targeting.
The latter can be supported later,
maybe via a plugin.

1. Create DMG file containing the application bundle from the previous stage.

   For consideration:

   * Include a link to the ``Applications`` directory.
   * Have it displayed in a nice visual layout.
   * When opened,
     optionally require accepting a license before mounting.

   How to do this:

   * Run the ``hdiutil`` command with the proper arguments.
   * Use `dmgbuild <https://pypi.org/project/dmgbuild/>`_.

   Eventually useful:

   * Adding a license file to a DMG using the ``rez`` command:
     `article <https://thehobbsfamily.net/archive2011/adding-software-license-agreement-dmg-file/>`_ and
     `code <https://bitbucket.org/jaredhobbs/pyhacker/raw/master/licenseDMG.py>`_
     (requires XCode Command Line tools to be installed,
     but then again so will signing and notarization).


On Windows:

There are two common ways of distributing installable programs:
``setup.exe``-like installers, and MSI files.
I tend to prefer the latter because they are
`natively supported <https://docs.microsoft.com/en-us/windows/win32/msi/windows-installer-portal>`_,
but I suppose supporting both is feasible given that,
up until now,
Mu has been distributed with a ``setup.exe``-like installer --
so there's that!
Food for thought.

AFAICT,
there are no native installer creation tools on Windows.
To create ``setup.exe``-like installers
either `NSIS <https://nsis.sourceforge.io/Main_Page>`_ or
`Inno Setup <https://jrsoftware.org/isinfo.php>`_
can be used,
and create MSI installer files,
the `WiX toolset <https://wixtoolset.org>`_
can be used, instead.

Regardless of the case,
the general procedure will be:

1. Create an input file with the necessary packaging specification,
   per the selected tool,
   maybe off a template.

2. Run the tool with that.



.. _things-wed-like-now:

Things we'd like now
--------------------

* Package `Mu Editor <https://codewith.mu/>`_
  for current macOS and Windows versions,
  into commonly used single file downloads for software distribution and installation..

  * Let's go with DMG files for macOS.
  * Windows needs thinking and experimentation, maybe.
  * Implies supporting `PyQt5 <https://pypi.org/project/PyQt5/>`_ based applications.
  * Extra: let's support
    `tkinter <https://docs.python.org/3/library/tkinter.html>`_ based ones too.

* Packaged distributions should be signed/notarized per platform requirements.

* Packaging with/under `CPython <https://www.python.org/>`_ 3.7 and 3.8.

* Distributable artifacts optionally ask for license agreement,
  during the installation.

* Can work offline,
  as far as platform signing/notarization requirements allow
  (but will require some initial "online time").



Things that need thinking now
-----------------------------

* Support 32-bit Windows or go 64-bit only?
* Go for Windows ``setup.exe``-like installers or MSI based ones, on Windows?
* The packaging process varies depending on several things:
  platform, final artifact "kind", and probably many more,
  yet to be identified.
  Let's have ``pup`` be extendable via plugins.

  * Could ``pup`` just be the *engine*,
    and packaging implementations be exclusively implemented by plugins?
    Maybe,
    as long as ``pup`` itself includes a set of *core plugins* that solve
    (most?) of the things "we'd like now",
    listed above.

  * Are we reinventing
    `make <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/make.html>`_?
    Can we build on top of
    `tox <https://pypi.org/project/tox/>`_
    or `nox <https://pypi.org/project/nox/>`_?
    Something else?



Things we'd like later
----------------------

* Linux Snap, Flatpak, AppImage (no idea what I'm talking about here!). :)
* Support current CPython: soon to be 3.9, then 3.10, and so on.
* GUIs built on top of
  `pygame <https://pypi.org/project/pygame/>`_,
  `pgzero <https://pypi.org/project/pgzero/>`_,
  `pyside2 <https://pypi.org/project/PySide2/>`_,
  `kivy <https://pypi.org/project/Kivy/>`_,
  `arcade <https://pypi.org/project/arcade/>`_.
* Direct to "store" publishing.
* If it's ``pip install``-able,
  it should be ``pup`` packageable.
* Given that ``pup`` will work hard to make things relocatable,
  producing "portable applications",
  that don't require installation on Windows,
  should be easy -- we want that.
* ``pup`` should not only be a CLI tool,
  but also a library with a stable API that other programs can use.
  How cool will it be when Mu itself gains a "package button"
  to help beginner's share their projects with friends and family? :)
  (yes, huge challenges here, especially WRT signing and cross-platform-ness).


Things that need thought, later
-------------------------------

* Installer and license agreement localization.
* Cross-platform packaging.
  Challenges:

  * Cross-platform ``pip install``-ing.
  * Cross-platform signing, notarizing and, ultimately, "store" publishing.

