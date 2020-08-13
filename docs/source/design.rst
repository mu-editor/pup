Design
======

From the notes in :doc:`thoughts`
it is clear that going for a plugin-supported design
seems desirable:
this should allow adderssing unforeseen packaging scenarios,
while at the same time forcing a cleaner design from the start.

What's a Plugin, then?
----------------------

We are calling *plugin* to a self-contained piece of code that,
maybe among other things:

* Is developed and distributed independently of ``pup``.
* Is written against a documented and stable ``pup`` Python plugin API.
* Will be discovered automatically by ``pup`` at runtime.
* Will be used by ``pup``,
  automatically or not,
  depending on the plugin itself and, maybe,
  on user/caller-provided parameters.
  


Diving In
---------

Let's see how this could work by starting off with two questions:

* Which behaviours would we want to be pluggable vs. built-in to ``pup``?
* How are we going to implement such a pluggable design?


Pluggable Behaviour Candidates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* **Stages and Steps**

  From the :doc:`thoughts` section,
  it is not clear yet
  whether the foreseen *stages and steps* structure is fixed or not.
  It does,
  however,
  seem like a very good idea to have such structure be pluggable.
  With that,
  the packaging process is "just" completing each step,
  in each stage,
  in the defined sequence.

  One question that arises is
  whether we just want to support a full *stages and steps* spec from a given plugin,
  or if we can support incremental changes to such an existing structure --
  the latter does not seem obvious,
  at first sight.

* **Execution Steps**

  By definition,
  these will vary,
  at least,
  by platform.
  Most probably they will vary with other factors,
  so these must be pluggable.

  The way to match pluggable *stages and steps* structures with
  pluggable *execution step* implementation is to be defined,
  but will probably be name-based. 

* **File Downloads**

  It is very likely that,
  when executing a particular packaging step,
  ``pup`` will need to download a file from somewhere.

  Let's not hardcode that.
  Keeping it pluggable should allow downloading files with protocols other than,
  say,
  HTTP only
  (yep, someone will want to grab files from S3, someday, won't they?).


* **Platform Directories**

  Will ``pup`` be configurable?
  Will it produce logs?
  Will it cache downloaded files?

  The answer to these is "probably yes" and,
  in that sense,
  where to keep such files will vary according to platform conventions.
  Keeping this pluggable will allow ``pup`` to support other platforms,
  including ones that are yet to be created.


*[there will be more entires here, soon, I guess...]*


Implementing a Pluggable Behaviour
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Plugins will announce themselves via a single,
  documented,
  `setuptools <https://setuptools.readthedocs.io/>`_                    
  `entry point <https://setuptools.readthedocs.io/en/latest/pkg_resources.html#entry-points>`_.

* ``pup`` will use `importlib-metadata <https://pypi.org/project/importlib-metadata/>`_
  to figure out which plugins are available.

* ``pup`` will call the plugin entry point,
  asking it to "register itself" with ``pup``.
  In that process,
  the plugin will "tell" ``pup``
  what pluggable behaviour it implements.

* ``pup`` itself will bundle a set of plugins
  that implement the :ref:`things-wed-like-now`.



More Design
-----------

With the very high level pluggable design,
above,
let's explore how ``pup`` could work
and which fundamental concepts arise as we do that.

*[very very rough draft as a dump of thoughts]*

* We will need to have a "dispatcher" that calls plugin-provided behaviours.
* There will probably be some kind of "context" object passed around everywhere.
* Not sure how to handle conflicting plugins/behaviours:
  what to do if we have two options for an exectution step named,
  say,
  ``create-windows-setup-exe``,
  one using `NSIS <https://nsis.sourceforge.io/Main_Page>`_,
  the other useing `Inno Setup <https://jrsoftware.org/isinfo.php>`_?.
  Feels like a place where caller/user-provided parameters may be of use.
