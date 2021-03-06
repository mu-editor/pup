Thoughts
========

.. note::

   This is a somewhat open and in-progress section,
   by definition.
   As soon as development reaches a minimally mature state,
   it will probably be either dropped
   or evolve into some kind of roadmap/whish list --
   you have been warned! :)



Preliminary words on what ``pup`` should do and how it could work.
That should help:

* Determine usage patterns.

* Define fundamental concepts.

* Identify challenges and requirements.



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
  platform, final artifact "kind", and probably many more.
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

* What's the usage pattern?
  Do we want ``make``-like behaviour where dependencies are analysed
  and incremental "builds" are supported,
  or do we go for something simpler,
  more along the lines of "just do it all, please, I don't care about the details"?



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
* If it's ``pip install``-able,
  it should be ``pup`` packageable.
* Given that ``pup`` will probably make things relocatable,
  producing "portable Windows applications"
  (no installation needed)
  should be easy -- we want that.
* ``pup`` should not only be a CLI tool,
  but also a library with a stable API that other programs can use.
  How cool will it be when Mu itself gains a "package button"
  to help beginners share their projects with friends and family? :)
  (yes, huge challenges here, especially WRT signing and cross-platform-ness).
* Support running tests on the pre-packaged result:
  right before the final put-it-all-in-a-single-file stage,
  running under the to-be-distributed Python environment.
* Installer and license agreement localization.


Things that need thinking later
-------------------------------

* Direct to "store" publishing.
* Cross-platform packaging.
  Challenges:

  * Cross-platform ``pip install``-ing.
  * Cross-platform signing, notarizing and, ultimately, "store" publishing.



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

.. _stage_1:

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
   from :ref:`stage_1`
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
   from :ref:`stage_1`
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



Stage 3 | Single-file distributable artifact
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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



Possible Usage
--------------

Packaging
^^^^^^^^^

Keeping things simple and aligned with the things we want,
the basic,
"it just works" usage shall be::

    $ pup package <src>


Where:

* ``<src>`` will be a directory containing a ``pip install``-able application source.
  If omitted,
  the `CWD <https://en.wikipedia.org/wiki/Working_directory>`_ will be assumed.

* The final single-file artifact will be put into ``<src>/dist``,
  in a file named after the application,
  including its version and,
  maybe,
  some other meta-data:
  Python version,
  32/64 bitness,
  *Portable ZIP*- vs. *NSIS*- vs. *Inno Setup*-packaged,
  more?...

* Packaging will default to produce a packaged application for the same platform
  where the packaging process is run,
  bundling the same major version of Python.

* As the process progresses,
  one per-stage sub-directory will probably be created under ``<src>/build/pup``
  and left alone for later analysis, maybe.

Some optional/required parameters can be envisioned:

* If there are multiple output format options for the platform
  (Windows MSI vs. ``setup.exe``-based installer, for example),
  maybe a ``--output-format=<format>`` will be required
  (unless a default one is implemented).

* Signing will very probably require some kind of ``--signer=<whom>`` argument
  so that the correct code-signing certificate can be used
  (again,
  unless an effective default certificate identification mechanism is put in place)

* Not sure if a ``--preview`` / ``--flight-check`` option will be useful:
  maybe it could not only run a few validations,
  but also report on its decisions,
  displaying the metadata for the application to be packaged,
  which relocatable Python will be downloaded,
  (if any, otherwise, which cached version will be used),
  which final packaging format will be used,
  whether or not required third-party tools are found
  (say,
  *XCode Command Line Tools*, needed for signing on macOS,
  or *NSIS* or the *WiX toolset* for final Windows packaging,
  and more).
  On possibly very useful output could be the "packaging plan",
  as a series of *stages* and *steps*.
  
Interesting future options:

* ``--platform=<platform>`` should support the production of a foreign-platform
  single-file application distribution artifact.

Some thoughts:

* Running the packaging process
  up until a specific *stage* or *step* might be useful.

* Tracking cross-*stage*/*step* dependencies is very non-trivial:
  ``pup`` will probably not implement a ``make``-like behaviour.
  It will probably always "start from scratch".
  This raises the question:
  how should it behave when it finds the left-overs of a previous run,
  say,
  under the ``<src>/build/pup`` directory?
  


Testing
^^^^^^^

Testing the application under the packaged environment will be a valuable capability.
It might be triggered with::

    $ pup test <src>

...where the ``<src>`` argument will be optional as with the ``package`` command.

The process will probably need to:

1. Complete :ref:`stage_1`.
2. Then install any test dependencies on that environment.
3. Finally running them.

The way to handle the test dependency installation and test running is non-obvious,
for now. One possibility could be:

* Requiring that the application source specifies a pre-defined
  `setuptools extra <https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies>`_
  called ``dev`` (or ``test``, maybe?),
  declaring the test running dependencies.

* Having an optional ``--run-tests-with=<python-args>`` that would have ``pup``
  pick up on ``<python-args>`` and run the tests by calling the Python executable
  in the :ref:`stage_1` output directory,
  like ``.../python <python-args>``.
  This would support running:

  * `unittest <https://docs.python.org/3/library/unittest.html>`_-based tests
    with ``--run-tests-with='-m unittest'``,
  * `pytest <https://pypi.org/project/pytest/>`_-based tests
    with ``--run-tests-with='-m pytest'``,
  * `Twisted Trial <https://twistedmatrix.com/trac/wiki/TwistedTrial>`_-based tests
    with ``--run-tests-with='-m twisted.trial ...'``,
  * ...and more, I suppose.



Cleaning Up
^^^^^^^^^^^

We want ``pup`` to be a nice citizen to your filesystem layout and disk utilization so
a single command will used to remove files and directories produced by itself::

    $ pup cleanup

Removes the intermediate *build* directories.

Then, maybe the following options could be useful:

* ``--caches`` removing all cached files that were previously downloaded.
* ``--artifacts`` removing all ``pup``-produced artifacts.
* ``--build`` (would be the implicit default, per the note above: do we want that?)
* ``--all`` might be friendly, too.


More Thoughts
-------------

As progress is made,
maybe more thoughts are written down here.
Or maybe in other,
more specific sections.
We will see...
