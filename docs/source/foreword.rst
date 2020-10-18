Foreword
========

As I write these words,
I'm not really sure for how long ``pup`` will actually live --
let me be clear:
it's not that I don't think the `Mu Editor <https://codewith.mu/>`_,
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
