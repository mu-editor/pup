Development
===========

``pup`` is openly developed on `GitHub <https://github.com/mu-editor/pup>`_, following a process that strives to be:

* As simple as possible, but not simpler.
* Easy to understand.
* Structured.
* Flexible.

Substantiated contributions and discussions will be welcome.



Environment
-----------

Setting up a development environment should be done under a Python virtual environment:

.. code-block:: console

    $ git clone https://github.com/mu-editor/pup
    $ cd pup/
    $ pip install -e .[dev]


Building the documentation, which will be available under ``docs/build/html/``:

.. code-block:: console

    $ cd docs && make html



Process 
-------

GitHub Issues, Labels, Milestones, and Pull Requests are used to track ``pup`` development.

* Issues must be labelled and associated to a milestone.
* Pull Requests must reference, at least, one issue (and preferably only one).
* Pull Requests will not be merged if any of the GitHub checks fails.
* Pull Requests will not necessarily be merged if all of the GitHub checks pass.



Milestones
^^^^^^^^^^

The following `GitHub Milestones <https://github.com/mu-editor/pup/milestones>`_ are tracked:

==================  ================================================================================
:guilabel:`NEXT`    Issues and Pull Requests that will be included in the next release.
:guilabel:`LATER`   Issues and Pull Requests that will be worked on, but will not be included in the next release.
:guilabel:`TBD`     Issues and Pull Requests that will not be worked on until future decision.
==================  ================================================================================

.. note::
    Unassigned Issues will be assigned to the :guilabel:`TBD` milestone.

At release time:

* The :guilabel:`NEXT` milestone is renamed to the release version and closed.
* A new :guilabel:`NEXT` milestone is created, with no associated Issues.



Issues and Labels
^^^^^^^^^^^^^^^^^

Development issues are used to describe, specify, discuss, evaluate, and track ideas on proposed changes to ``pup``, and will be `labelled <https://github.com/mu-editor/pup/labels>`_ one of:

======================= =================================================================================
:guilabel:`enhancement` Describing a new feature or capability.
:guilabel:`bug`         Describing something that isn't working as documented.
:guilabel:`release`     Describing release process issues.
:guilabel:`maintenance` Describing other development related issues: refactors, automation, process, etc.
======================= =================================================================================


Non-labelled issues are assumed to be support-related.
They describe user experiences in using ``pup``,
and will generally fall into one of the
*"it doesn't work for me"* or *"it should do this new thing"* groups.
Triaging and in-issue will either close such issues or
label and associate them with a milestone,
integrating them into the development process.


General requirements:

* All issues should describe a single, actionable topic.

* Complex issues should be split into simpler, possibly related, issues.

* :guilabel:`enhancement` issues:

  * Must describe the use-case, benefits and tradeoffs.

  * If applicable,
    should include sample code/CLI usage
    demonstrating the enhancement in action.

* :guilabel:`bug` issues must:

  * Be explicitly reported against either the latest `PyPI released version <https://pypi.org/pypi/pup>`_ or the current `GitHub master branch <https://github.com/mu-editor/pup/tree/master>`_.

  * Describe the steps to reproduce the bug,
    ideally with a minimal code/CLI usage sample.

  * Describe the expected and actual results.

  * Include a reference to where the documentation is inconsistent with the actual results,
    or highlight the fact that the behaviour is non-documented.


* :guilabel:`maintenance` issues:

  * Must describe the purpose, benefits and trade-offs.



Pull Requests
^^^^^^^^^^^^^

Pull Requests are implementation proposals for previously identified and agreed to be addressed issues.  They are `tracked here <https://github.com/mu-editor/pup/pulls>`_ and:

* Must reference an existing, open issue, and preferably only one.
* May totally or partially contribute to closing the referenced open issue.
* Will not be merged if any of the GitHub checks fails.
* Will not necessarily be merged if all of the GitHub checks pass.
* Will not be labelled or assigned to a milestone.

.. note::

   **Issues** vs **Pull Requests**

   * Issues are used to describe, discuss, and specify ideas and concepts.
   
   * Pull Requests are used to propose, describe, and discuss
     the implementation of previously agreed-upon ideas in Issues.

   Please do not create Pull Requests
   without prior discussion and agreement in the context of a related Issue.
   It will make everybody's live easier!



Release Procedure
-----------------

Confirm that the :guilabel:`NEXT` milestone contains:

- No open issues.
- One or more closed issues, each associated with one or more merged Pull Requests.


Once confirmed, rename the :guilabel:`NEXT` milestone to :guilabel:`MAJOR.MINOR.MICRO` and create a new issue in it, labelled :guilabel:`release` and named "Release". Then:

- Update ``__version__`` in ``src/pup/__init__.py``.
- Confirm that the documentation builds successfully, making adjustments if needed.
- Update the :doc:`changelog`:

  - Run ``towncrier --draft`` and confirm the output.
  - If needed, add missing ``.deprecate``, ``.enhancement``, ``.bug`` or ``.other`` news-fragment files under ``docs/newsfragments``.
  - Once the draft output looks correct, run ``towncrier``.

- Commit the version, documentation and changelog changes, tagging it :guilabel:`MAJOR.MINOR.MICRO`.
- Create Pull Request against the "Release" issue.
- Once all the GitHub checks pass, merge the Pull Request.
- Update the local repository with the GitHub merged changes.
- Release in PyPI:

  - Install release dependencies:

    .. code-block:: console

        $ pip install -e .[release]

  - Build the release artifacts:

    .. code-block:: console

        $ rm -r build/ dist/
        $ python setup.py sdist bdist_wheel

  - Upload to test PyPI:

    .. code-block:: console

        $ twine upload -r test dist/pup-*

  - Test the installation into a freshly created virtual environment:

    .. code-block:: console

        $ pip install -i https://test.pypi.org/pypi pup

  - If ok, upload to PyPI:

    .. code-block:: console

        $ twine upload -r pypi dist/pup-*

  - Confirm the installation into a freshly created virtual environment:

    .. code-block:: console

        $ pip install pup

  - Lastly, cleanup again:

    .. code-block:: console

        $ rm -r build/ dist/

- Confirm the versioned documentation is available at `Read the Docs <https://pup.readthedocs.org/>`_.

- Close the :guilabel:`MAJOR.MINOR.MICRO` milestone.

- Lastly, create a new :guilabel:`NEXT` milestone.

