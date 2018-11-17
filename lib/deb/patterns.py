CONTROL="""Package: man-intrinsics
Version: %(version)s
Maintainer: %(maintainer)s
Section: developer
Priority: optional
Architecture: all
Description: The list of x86 instrinsics
%(details)s
"""

POSTINST="""#!/bin/sh
set -e
mandb
"""

POSTREMOVE=POSTINST
