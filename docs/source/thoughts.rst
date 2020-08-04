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

1. Lay a relocatable Python distribution in a *build* directory.

2. Use that Python distribution's ``pip`` to install the applicataion which,
   by definition, will be installed within that Python environment's ``site-packages``.

3. On ...

   * On macOS ...

   * On Windows ...

   * On Linux ...



.. admonition:: Notes

  Step 1.

  * Gregory Szorc's
    `Python Standalone Builds <https://python-build-standalone.readthedocs.io/>`_
    looks like a very good candidate.
    Preliminary testing showed it to work *out-of-the-box*. :)

  Step 2.

  * Assumes That we're packaging for the same platform we're running on.
    Otherwise, that Python distribution wouldn't be executable.

  * Requires that the application being packaged is ``pip install``-able.


  Step 3.

  * We will get to that.




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

