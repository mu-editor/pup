Thoughts
========

.. note::

   This is an early draft of a clearly *in progress* section, as of now.
   You have been warned! :)



Preliminary words on how ``pup`` could work. Should help:

* Determine usage patterns.

* Define fundamental concepts.

* Identify challenges.

* The overall development process.



Packaging a Python GUI Application
----------------------------------

*...aka, the famous last "how hard can it be?" words.*

A possible way to package a Python GUI application is as follows:

Stage 1
^^^^^^^

1. Lay a relocatable Python distribution in a *build* directory.

   Gregory Szorc's
   `Python Standalone Builds <https://python-build-standalone.readthedocs.io/>`_
   looks like a very good candidate.
   Preliminary ad-hoc testing showed it to work *out-of-the-box*,
   on both macOS and Windows --
   there's no motive to suspect that it won't work on Linux.

2. Use that Python distribution's ``pip`` to install the applicataion which,
   by definition, will be installed within that Python environment's ``site-packages``,
   along with its specified dependencies.

   Assumes that we're packaging for the same platform we're running on.
   Otherwise, that Python distribution wouldn't be executable.

   Requires that the application being packaged is ``pip install``-able
   and declares one `setuptools <https://setuptools.readthedocs.io/>`_
   `entry point <https://setuptools.readthedocs.io/en/latest/pkg_resources.html#entry-points>`_.


At this point,
the application should be launchable from a CLI,
by running the ``pip install``-ed entry point executable
within the relocatable Python distribution.


Stage 2
^^^^^^^

On macOS:

1. Create a bare-bones `application bundle <https://developer.apple.com/library/archive/documentation/CoreFoundation/Conceptual/CFBundles/BundleTypes/BundleTypes.html>`_,
   maybe off of a template.

   Application bundles are directories
   containing a set of predefined files and sub-directories,
   holding everything needed to run the application:
   executable, libraries, resources, etc.
   For end users,
   application bundles look like files in the Finder.

2. Copy the relocatable Python distribution
   from Stage 1
   into the application bundle.

3. Create the application bundle's executable,
   under the ``MacOS`` sub-directory,
   as a shell-script that runs the application's entry point executable.

   Care must be taken to avoid having absolute paths,
   which the application's entry point executable probably includes.


At this point,
the application should be launchable from the Finder.


On Windows:

1. Create an appliction directory layout,
   somewhat inspired on macOS's application bundles.

2. Copy the relocatable Python distribution
   from Stage 1
   into it.

3. Create the application's *explorer clickable thing* as a
   `shell link <https://docs.microsoft.com/en-us/windows/win32/shell/links>`_
   in the root of the application directory layout.

   It should either run the application's entry point executable or,
   alternatively,
   run the relocatable ``python`` binary with a ``-m <application>`` argument.
   Either of these options still needs evaluation:
   on one hand,
   we're not sure yet if the application's entry point executable is relocatable
   (thus failing to run when the whole application directory is moved);
   on the other,
   going ``python -m <application>`` imposes further requirements on the way
   the application is created.

   All in all, this step may not be strictly needed,
   given that on a later stage everything will be bundled into an installable file
   that itself will be responsible for creating a *Start Menu* link,
   much like this one.


On Linux:

1. *[TBD]*

2. ...

3. *[profit?!]* :)




Things we'd like soon
---------------------

*[grab them from the README and expand]*



Things we'd like later
----------------------

*[grab them from the README and expand]*


Things that need serious thought
--------------------------------

*[grab them from the README and expand]*




About Plugins
-------------

.. note::

   More on this later. Just writing down the basic idea.


* Plugins announce themselves via ``setuptools`` *entrypoints*.

* We will use ``importlib-metadata`` to figure out which plugins are available.

* ``pup`` will then import and call the published entry points,
  depending on its configuration/invocation.

