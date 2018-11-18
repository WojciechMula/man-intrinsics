ARCH_HEADER=R""".SH INSTRUCTION PARAMETERS
"""

ARCH_TABLE_START_LONG=""".TS
allbox;
c s s s s
l r r r l.
"""

ARCH_TABLE_START_SHORT=""".TS
allbox;
c s s s
l r r r.
"""

ARCH_TABLE_HEADER_LONG="""%s
Architecture\tLatency\tThroughput\tuops\tuops details
"""

ARCH_TABLE_HEADER_SHORT="""%s
Architecture\tLatency\tThroughput\tuops
"""

ARCH_TABLE_ROW_LONG="""%(architecture)s\t%(latency)s\t%(throughput)0.2f\t%(uops)d\t%(uops_details)s
"""

ARCH_TABLE_ROW_SHORT="""%(architecture)s\t%(latency)s\t%(throughput)0.2f\t%(uops)d
"""

ARCH_TABLE_END=""".TE
"""

