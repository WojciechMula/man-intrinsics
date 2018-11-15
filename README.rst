================================================================================
            Manual pages for Intel Intrinsics Guide
================================================================================

Intel provides great and well designed site `Intrinsics Guide`__ that gives
a programmer the full list of x86 instrinsics functions. I use the page often,
but there are days when I'm offline and then miss ability to do quick searches.

__ https://software.intel.com/sites/landingpage/IntrinsicsGuide/.

This repository contains a python script which converts data used by *Intrinsics
Guide* and uops.info into set of unix manual pages.

*Intrinsics Guide* loads a huge XML file, just download that file and feed the
generator.

Invocation::

    python main.py guide.xml uops.info destination-dir


See also:

* https://github.com/Wunkolo/Intriman --- similar project, targeting more
  output formats
* https://github.com/HJLebbink/asm-dude/wiki --- data extracted from the
  official Intel documents
