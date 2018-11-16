class Instruction(object):
    __slots__ = (
        'name',
        'form',
        'cpuid',
        'measurements',
    )

    def __init__(self):
        self.name  = None
        self.form  = None
        self.cpuid = None
        self.measurements = []


    def __len__(self):
        return self.measurements


    def __str__(self):
        return '%s: %s' % (self.form, self.measurements)

    __repr__ = __str__


class Measurement(object):
    __slots__ = (
        'latency',
        'throughput',
        'total_uops',
        'uops_details',
    )

    def __init__(self):
        self.latency      = None
        self.throughput   = None
        self.total_uops   = None
        self.uops_details = None


    def __str__(self):
        return '<Measurement: %s, %s, %s, %s>' % \
               (self.latency, self.throughput, self.total_uops, self.uops_details)

    __repr__ = __str__


class PortDetail(object):
    __slots__ = (
        'ports',
        'uops',
    )

    def __init__(self):
        self.ports = None
        self.uops  = None


    def __str__(self):
        return '<p%s: %d>' % (self.ports, self.uops)

    __repr__ = __str__


class IACAMeasurements(Measurement):
    __slots__ = (
        'latency',
        'throughput',
        'total_uops',
        'uops_details',
        'version'
    )

    def __init__(self):
        super(Measurement, self).__init__()

    def __str__(self):
        return '<IACA %s: %s, %s, %s, %s>' % \
        (self.version, self.latency, self.throughput, self.total_uops, self.uops_details)
