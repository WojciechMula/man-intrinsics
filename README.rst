================================================================================
            Manual pages for Intel Intrinsics Guide
================================================================================

Intel provides great and well designed site `Intrinsics Guide`__ that gives
a programmer the full list of x86 instrinsics functions. I use the page often,
but there are days when I'm offline and then miss ability to do quick searches.

__ https://software.intel.com/sites/landingpage/IntrinsicsGuide/.

This repository contains a python script which converts data used by Intrinsics
Guide into set of unix manual pages. *Intrinsics Guide* loads a huge XML file,
just download that file and feed the generator.

Invocation::

    python main path-to-data-xml destination-dir


TODO
--------------------------------------------------------------------------------

* fix ``[round_note]`` references in AVX512 descriptions
