MAN_GROUP='7'

MAIN=R""".\" auto-generated file
.TH %(technology)s %(group)s %(date)s "Version %(version)s" "The list of x86 intrinsics"

.SH NAME
.EX
#include <%(include)s>

%(rettype)s \fB%(name)s\fP(%(arguments)s);
.EE

.SH DESCRIPTION
%(description)s
"""

NO_INSTRUCTION_NOTE=R""".PP
\fBNote\fP: this function might not map directly into a CPU instruction.
"""

CATEGORY_AND_TYPE=R""".PP
Category: \fI%(category)s\fP, \fI%(type)s\fP
"""

CATEGORY=R""".PP
Category: \fI%(category)s\fI
"""

OPERATION=R""".SH OPERATION
.EX
%(operation)s
.EE
"""


INSTRUCTION_HEADER=R""".SH CPU INSTRUCTION
.EX
"""

INSTRUCTION_ENTRY="""%(instruction)s %(arguments)s
"""

INSTRUCTION_TAIL=""".EE
"""


CPUID_HEADER=R""".SH CPUID FLAGS
.PP
"""

CPUID_ENTRY=R""".br
\fT%(flag)s\fP%(last)s
"""

SEE_ALSO_HEADER=R""".SH SEE ALSO
"""

SEE_ALSO_ENTRY=R""".BR %(name)s (%(group)s)%(last)s
"""
