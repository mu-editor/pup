``pup`` | Python Mu Packager
============================

``pup`` is (in the early stages of development and risks becoming) a packaging tool
for GUI programs written in Python.

Fundamentally,
its *raison d'être* is producing macOS and Windows native packages
for distributing the `Mu Editor <https://codewith.mu/>`_
to Python beginners around the world.
As a by-product of that,
it might become effective at packaging
generic Python written GUI programs.
If that ever becomes the case,
then great.
Otherwise,
that's fine too.

The purpose,
again,
is to package the `Mu Editor`_
for macOS and Windows distribution.



Foreword
--------

As I write these words,
I'm not really sure for how long ``pup`` will actually live --
let me be clear:
it's not that I don't think the Mu Editor,
in particular,
and the world of Python GUI applications in general
don't need a simple and effective native packager,
I honestly do;
moreover,
I do believe that there should be more diversity and more GUI applications
-- even if *ugly* (whatever that means!) --
in contrast with the trends towards web-based ones,
like we have been observing throughout the last decade or so.

As was saying, I'm not really sure for how long ``pup`` will live.
Why?
Mostly because ``pup`` is kind of a conceptual fork of
`briefcase <https://pypi.org/project/briefcase/>`_,
up to a point.
I gave this idea lots of thought and figured out that,
for the near-term future,
creating ``pup`` would be the best option for packaging Mu.
Later it its life,
it may make sense to integrate its "tricks"
into `briefcase <https://pypi.org/project/briefcase/>`_,
which is a more generic and mature tool,
with much higher aspirations.

The fact of the matter is that Mu itself is a very particular kind of GUI program:
it is a program to create programs,
a program that runs and debugs programs,
a program that brings in third-party dependencies,
a program that uploads code to micro-controllers,
and so much more.

Mu is at a development stage
where several things "must" happen somewhat fast enough:
for one,
robust support for bringing in third-party packages from PyPI,
something that mostly works on Windows and fails miserably on macOS,
already has a re-architected solution that now unfortunatelly fails
when packaged natively --
we could,
of course,
hack our way through the currently existing,
somewhat brittle and inconsistent Mu packaging tools and scripts
to fix that.
Then,
of course,
we're one year (!!!) late
to the macOS application notarization requirement race (party?).
The end result is as expected:
beginner programmers having wierd issues and unnecessary barriers
with Mu on their computers.
Completely the opposite of Mu's purpose!

Creating ``pup`` will allow the Mu team
to fully decouple the packaging efforts
from Mu's own development while,
at the same time,
simplifying the autonomous and hopefully fast-paced development
of a fully automatable packaging tool for its own purposes.
In the near term,
the Holy Grail
is for Nicholas
to be able
to type something like ``pup go`` on on his development environment
and have it automatically produce the final Windows or macOS distribution artifacts:
signed,
notarized,
with all the required "seals",
and working as well as it works for any of us under our development systems:
in other words,
"works for me"-everywhere!

"How hard can it be?" :)



Wish List
---------

Near term:

* If it's ``pip install``-able it should be ``pup package``-able.

* Distributions must have exactly one `setuptools <https://setuptools.readthedocs.io/>`_ `entry point <https://setuptools.readthedocs.io/en/latest/pkg_resources.html#entry-points>`_.

* Supports:

  * Recent Windows and macOS operating systems.
  * `CPython <https://www.python.org/>`_ 3.7 and 3.8.
  * GUIs built on top of
    `tkinter <https://docs.python.org/3/library/tkinter.html>`_ and
    `pyqt5 <https://pypi.org/project/PyQt5/>`_.
  * Signing/notarizing binaries and installers per platform requirements.

Needs thinking:

* Support 32 bit Windows or go 64 bit only?
* Support NSIS-based Windows installers? MSI ones? Both?
* Windows tend to need installers: consider localization (argh!).
* macOS distributions should be DMG file based.
* Probably want to go plugin-based.
* Can work offline, as far as platform signing/notarization requirements allow.
* Installers/DMGs should have a LICENSE for the user to read/agree with.


Later:

* Supports:

  * Linux Snap, Flatpak, AppImage (no idea what I'm talking about here!). :)
  * Current CPython.
  * GUIs built on top of
    `pygame <https://pypi.org/project/pygame/>`_,
    `pgzero <https://pypi.org/project/pgzero/>`_,
    `pyside2 <https://pypi.org/project/PySide2/>`_,
    `kivy <https://pypi.org/project/Kivy/>`_,
    `arcade <https://pypi.org/project/arcade/>`_.

* Direct to "store" publishing.


Non-trivial at first sight:

* Cross-platform packaging. Challenges:

  * Cross-platform ``pip installing``.
  * Cross-platform signing.



More
----

To learn more about ``pup`` you will have to wait a bit.
Development is going forward in the open
on GitHub at https://github.com/mu-editor/pup/.

.. marker-end-welcome-dont-remove



Installation
------------

``pup`` will be distributed via `PyPI <https://pypi.org/pypi/pup>`_.
Install it with:

.. code-block:: console

	$ pip install pup



Thanks
------

.. marker-start-thanks-dont-remove

- Nicholas Tollervey for the amazing `Mu Editor`_.

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

.. marker-end-thanks-dont-remove



About
-----

.. marker-start-about-dont-remove

``pup`` is in the process of being created by Tiago Montes,
with the wonderful support of the Mu development team.

.. marker-end-about-dont-remove

