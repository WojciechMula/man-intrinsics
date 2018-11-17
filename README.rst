================================================================================
            Manual pages for Intel Intrinsics Guide
================================================================================

.. contents::

Introduction
--------------------------------------------------------------------------------

Intel provides great and well designed site `Intrinsics Guide`__ that gives
a programmer the full list of x86 intrinsics functions. I use the page often,
but there are days when I'm offline and then miss ability to do quick searches.

__ https://software.intel.com/sites/landingpage/IntrinsicsGuide/.

This repository contains a python script which creates a set of Unix manual
pages. It uses data from *Intrinsics Guide* and optionally from `uops.info`__.
The latter provides detailed parameters of CPU instructions for various
architectures.

__ http://uops.info/


Generation
--------------------------------------------------------------------------------

*Intrinsics Guide* loads a huge XML file, just download that file and feed the
generator. *uops.info* provides a direct link to download their database, also
in XML format.

Invocation::

    $ ./main.py -g guide.xml -o destination-dir

or::

    $ ./main.py -g guide.xml -u uops.info.xml -o destination-dir


Limiting ISA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Intrinsics Guide** lists all SIMD (and not only SIMD) instructions. However,
MMX is not used anymore; likewise, KNC wasn't a very widespread technology.

It's possible to select which instructions include or exclude. The option
``--isa`` selects ISA to generate, the option ``--omit-isa`` excludes ISA.
Both can be passed as many times as it's needed and both accept a string,
ISA symbol, as argument

To obtain the list of meaningful ISA symbols use ``--dump-isa``.

Examples::

    $ ./main.py -g guide.xml --dump-isa
    List of ISAs defined in guide.xml: ..., MMX, ..., SSE, SSE2, ...

    # will generate man pages only for instrctions from SSE and SSE2
    $ ./main.py -g guide.xml --isa=SSE --isa=SSE2 -o output-dir

    # will generate man pages for all instructions except MMX
    $ ./main.py -g guide.xml --omit-isa=SSE -o output-dir


Limiting architectures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Database from **uops.info** provides parameters for several architectures,
some of them outdated. It's possible to select which architecture include
(with option ``--arch``) or exclude (with option ``--omit-arch``).
The options can be passed as many times as it's needed, both accept a string,
arch name or symbol.

The list of symbol and names is displayed by option ``--dump-arch``.

Examples::

    # will include details for architectures Haswell, Skylake and SkylakeX
    $ ./main.py -g guide.xml -u uops.xml -o output-dir --arch=HSW --arch=skylake --arch=SkylakeX

    # will exclude details for Westmere
    $ ./main.py -g guide.xml -o output-dir --omit-arch=Westmere


Building .deb packages
--------------------------------------------------------------------------------

To create special .deb files (control, postinst, postrm) pass option ``--deb``
with the destination directory. Please refer to sample ``Makefile.deb`` for details.

Example::

    $ ln -s your-guide.xml guide.xml
    $ ln -s your-uops.xml uops.xml

    # optionally set extra options for script
    $ export MANOPTIONS=''

    $ make -f Makefile.deb
    # it'll take some time

    $ ls man*.deb
    man-intrinsics_<guide-version>_all.deb

You can install the deb file with ``dpkg -i file.deb``.


See also
--------------------------------------------------------------------------------

* https://github.com/Wunkolo/Intriman --- similar project, targeting more
  output formats
* https://github.com/HJLebbink/asm-dude/wiki --- data extracted from the
  official Intel documents
