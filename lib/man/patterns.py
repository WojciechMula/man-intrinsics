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

CATEGORY_HEADER=R""".PP
Category: %s
"""

CATEGORY_ENTRY=R"\fI%s\fP"

ROUND_NOTE=R""".SH ROUNDING NOTE
.PP
The parameter \fBrounding\fP can be one of
.PP
\fT_MM_FROUND_TO_NEAREST_INT |_MM_FROUND_NO_EXC\fP
.RS 4
round to nearest; disable exceptions
.RE
\fT_MM_FROUND_TO_NEG_INF |_MM_FROUND_NO_EXC\fP
.RS 4
round down; disable exceptions
.RE
\fT_MM_FROUND_TO_POS_INF |_MM_FROUND_NO_EXC\fP
.RS 4
round up; disable exceptions
.RE
\fT_MM_FROUND_TO_ZERO |_MM_FROUND_NO_EXC\fP
.RS 4
truncate; disable exceptions
.RE
\fT_MM_FROUND_CUR_DIRECTION\fP
.RS 4
use settings from flag \fTMXCSR.RC\fP
.RE
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

ARCH_HEADER=R""".SH INSTRUCTION PARAMETERS
"""

ARCH_TABLE_START=""".TS
allbox;
c s s s s
l r r r l.
"""

ARCH_TABLE_HEADER="""%s
Architecture\tLatency\tThroughput\tuops\tuops details
"""

ARCH_TABLE_ROW="""%(architecture)s\t%(latency)s\t%(throughput)0.2f\t%(uops)d\t%(uops_details)s
"""

ARCH_TABLE_END=""".TE
"""


SEE_ALSO_HEADER=R""".SH SEE ALSO
"""

SEE_ALSO_ENTRY=R""".BR %(name)s (%(group)s)%(last)s
"""
