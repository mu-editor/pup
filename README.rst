``pup`` | Pluggable Micro Packager
==================================

``pup`` is (in the early stages of development and risks becoming) a packaging tool
for GUI programs written in Python.

Fundamentally,
its *raison d'être* is producing macOS and Windows native packages
for distributing the `Mu Editor <https://codewith.mu/>`_
to Python beginners around the world.
As a by-product of that,
it will very likely become effective at packaging
generic Python written GUI programs.
If that ever becomes the case,
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
and `puppy <https://github.com/tmontes/puppy/>`_ into:

* Native Windows applications, bundled in relocatable directories.
* Native macOS relocatable ``.app`` application bundles,
  properly signed and notarized as required for distribution.

It might work with any Python GUI application that:

* Runs on Python 3.7 or 3.8.
* Is ``pip``-installable (no need to be on PyPI, though).
* Is launchable from the CLI with ``python -m <launch-module>``.



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

        $ pup package <pip-installable-source>


* Assumes that the application is launchable with ``python -m <name>``,
  where ``<name>`` is extracted from the wheel metadata of a wheel created
  from ``<pip-installable-source>``.
  If the name of the launch module does not match that,
  the ``--launch-module <launch-module-name>`` CLI option should be provided.
* In the first run,
  ``pup`` will download a distributable Python Runtime from the
  `Python Build Standalone <https://python-build-standalone.readthedocs.io/>`_
  project.
  Subsequent runs will use a locally cached version of that.
* ``pup`` logs its progress to STDERR,
  with fewer per-event details when it's a TTY.
  The logging level defaults to ``INFO`` and can be changed
  with either the ``--log-level`` CLI option,
  or by setting the ``PUP_LOG_LEVEL`` environment variable.
* The resulting artifact will be under ``./build/pup/``.


Packaging the Mu Editor on Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

        > pup package --launch-module=mu <path-to-local-mu-git-repo-root>


* The resulting packaged application will be the ``./build/pup/<name>-<version>/``
  directory which contains a GUI-clickable script that launches the application.

* Creating an ZIP archive of that directory and distributing it should work,
  up to a point,
  given that no code/package signing is implemented yet.





Packaging the Mu Editor on macOS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

        $ export PUP_SIGNING_IDENTITY=<signer>
        $ export PUP_NOTARIZE_USER=<user>
        $ export PUP_NOTARIZE_PASSWORD=<asp>
        $ pup package --launch-module=mu <path-to-local-mu-git-repo-root>





More
----

To learn more about ``pup``
refer to the `online documentation <https://pup.readthedocs.io/>`_:
at this early stage,
it is mostly a collection
of thoughts and ideas
around behaviour, requirements, and internal design.
Development moves forward
on GitHub at https://github.com/mu-editor/pup/.


.. marker-end-welcome-dont-remove


Thanks
------

.. marker-start-thanks-dont-remove

- Nicholas Tollervey for the amazing `Mu Editor <https://codewith.mu/>`_.

- The Mu contributors I've been having the privilege of working more directly with,
  Carlos Pereira Atencio, Martin Dybdal, and Tim Golden, as well as the others
  whom I haven't met yet but whose contributions I highly respect.

- To Russell Keith-Magee for the inspiring `BeeWare <https://beeware.org>`_ project
  and, in particular, for `briefcase <https://pypi.org/project/briefcase/>`_ that
  being used as the packaging tool for Mu on macOS as of this writing, serves as a
  great inspiration to ``pup``.

- To Gregory Szorc for the incredible
  `Python Standalone Builds <https://python-build-standalone.readthedocs.io/>`_
  project,
  on top of which we plan to package redistributable Python GUI applications.

- To Donald Stufft for letting us pick up the ``pup`` name in PyPI.

- To Glyph Lefkowitz for the very useful,
  high quality `Tips And Tricks for Shipping a PyGame App on the Mac
  <https://glyph.twistedmatrix.com/2018/01/shipping-pygame-mac-app.html>`_
  article,
  and for his generous hands-on involvement in the first-steps of ``pup``'s take
  on the subject `in this issue <https://github.com/mu-editor/pup/issues/43>`_.

.. marker-end-thanks-dont-remove



About
-----

.. marker-start-about-dont-remove

``pup`` is in the process of being created by Tiago Montes,
with the wonderful support of the Mu development team.

.. marker-end-about-dont-remove

