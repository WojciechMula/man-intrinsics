================================================================================
            Manual pages for Intel Intrinsics Guide
================================================================================

Intel provides great and well designed site `Intrinsics Guide`__ that gives
a programmer the full list of x86 intrinsics functions. I use the page often,
but there are days when I'm offline and then miss ability to do quick searches.

__ https://software.intel.com/sites/landingpage/IntrinsicsGuide/.

This repository contains a python script which creates a set of Unix manual
pages. It uses data from *Intrinsics Guide* and optionally from `uops.info`__.
The latter provides detailed parameters of CPU instructions for various
architectures.

__ http://uops.info/

*Intrinsics Guide* loads a huge XML file, just download that file and feed the
generator. *uops.info* provides a direct link to download their database, also
in XML format.

Invocation::

    $ ./main.py -g guide.xml -o destination-dir

or::

    $ ./main.py -g guide.xml -u uops.info.xml -o destination-dir


See also:

* https://github.com/Wunkolo/Intriman --- similar project, targeting more
  output formats
* https://github.com/HJLebbink/asm-dude/wiki --- data extracted from the
  official Intel documents
