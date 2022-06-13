Linux AppImage
--------------

Current support for building Linux AppImages is in its early stages of development.

A few notes:

* Creating AppImages requires passing the ``--icon-path`` option,
  pointing to a PNG file to be used as an icon.

* The required ``.desktop`` file,
  embedded into the AppImage,
  currently has a hard-coded category of ``Education``.

* By default,
  ``pup`` uses an x86-64 AppImageTool from `<https://github.com/AppImage/AppImageKit/releases>`_.
  It can be overridden by setting the ``PUP_AIT_URL`` environment variable
  to the URL of an alternative AppImageTool AppImage.
