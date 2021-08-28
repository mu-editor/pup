Windows MSI
-----------

Capabilities
~~~~~~~~~~~~

Two different user interfaces are used:

  * Minimal, with a single progress bar, by default.
  * Multi-step, displaying the license text, requiring it to be accepted
    before continuing, supporting post-install auto-launch.

The minimal UI is used when the ``--license-path`` CLI option is omitted.


Versions
~~~~~~~~

There are significant semantic gaps between
`PEP 440 <https://www.python.org/dev/peps/pep-0440/>`_ and
`MSI package versions <https://docs.microsoft.com/en-us/windows/win32/msi/productversion>`_.

In the worst case scenario,
they prevent packaging to MSI.
In less drastic cases,
the end-user process of upgrading to/from non-final PEP-440 versions might be affected.

Things you want to know:

* PEP-440 versions support pre/post release segments,
  like ``a1``, ``b1``, or ``.post1``,
  used as suffixes to the common ``X.Y.Z`` version strings.
  Such segments are not supported by the MSI format
  and ``pup`` strips them away,
  logging a warning message like:
  
  .. code-block:: none

      W Version '2.0.0a1' not MSI supported: using '2.0.0'.

  The MSI filename,
  installer GUI,
  and installed program name --
  under *Programs and Features* --
  will still include the full PEP-440 version string.

* PEP-440 versions support more than three dot-separated number versions,
  like ``1.2.3.4``,
  for example.
  The MSI format only supports three and,
  again,
  in these cases,
  ``pup`` strips away the rightmost PEP-440 ones,
  logging a warning message like:

  .. code-block:: none

      W Version '1.2.3.4' not MSI supported: using '1.2.3'.

  As above,
  the MSI filename,
  installer GUI,
  and installed program name --
  under *Programs and Features* --
  will still include the full PEP-440 version string.

* MSI versions are structured ``MAJOR.MINOR.BUILD`` where
  ``MAJOR`` and ``MINOR`` must be integers between 0 and 255,
  and ``BUILD`` must be an integer between 0 and 65535.

  As of this writing,
  ``pup`` fails to handle such a limitation,
  other than the fact that the WiX toolset error
  is logged by ``pup`` at info level and,
  unsurprisingly,
  no MSI file is actually produced --
  tracked in `GitHub issue #166 <https://github.com/mu-editor/pup/issues/166>`_.


Upgrading to/from non-final PEP-440 versions
""""""""""""""""""""""""""""""""""""""""""""

Given that four distinct PEP-440 versions
like the still-buggy ``1.1.0b1``,
the not-so-bad ``1.1.0b2``,
the near-final ``1.1.0rc1``,
and the final ``1.1.0``
all lead to the same ``1.1.0`` MSI version,
**the common end-user upgrade process does not work** --
installing ``1.1.0b2`` over ``1.1.0b1``,
for example,
or ``1.1.0`` over any of the others.

This is due to the fact that the Windows installer cannot differentiate them.
Upgrading to/from such non-final PEP-440 versions,
thus,
requires a two step process:

* Uninstalling the older, installed version first.
* Installing the newer version later.

Failing to do that might lead to all sorts of unexpected behaviours including
having multiple entries of a given program under the *Programs and Features*
Windows dialog,
or (dangerous!)
having sets of non-consistent on disk files,
obtained from different versions of the software.
