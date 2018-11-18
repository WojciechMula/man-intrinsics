from uops_patterns import *

class Generate(object):
    def __init__(self, options, datasource):
        self.options = options
        self.datasource = datasource
        self.arch_db = datasource.get_architecture_details()

        if self.options.uops_ports:
            self.TABLE_START  = ARCH_TABLE_START_LONG
            self.TABLE_HEADER = ARCH_TABLE_HEADER_LONG
            self.TABLE_ROW    = ARCH_TABLE_ROW_LONG
        else:
            self.TABLE_START  = ARCH_TABLE_START_SHORT
            self.TABLE_HEADER = ARCH_TABLE_HEADER_SHORT
            self.TABLE_ROW    = ARCH_TABLE_ROW_SHORT


    def generate(self, entry):
        res = ''

        arch_details = self.get_details(entry)
        if not arch_details:
            return res

        rows = 0
        res += ARCH_HEADER
        for instruction in arch_details:
            res += self.TABLE_START
            res += self.TABLE_HEADER % instruction.form
            for arch, measurements in instruction.measurements.iteritems():
                if not self.datasource.filter_by_arch(arch):
                    continue

                arch_fmt = format_architecture(arch)
                for measurement in measurements:
                    data = {
                        'architecture'  : arch_fmt,
                        'latency'       : format_latency(measurement.latency),
                        'throughput'    : measurement.throughput,
                        'uops'          : measurement.total_uops,
                        'uops_details'  : format_port_details(measurement.uops_details),
                    }

                    res += self.TABLE_ROW % data
                    rows += 1

            res += ARCH_TABLE_END

        if rows > 0:
            return res
        else:
            return ''
       

    def get_details(self, entry):
        result = []
        for instruction, _ in entry.instructions:
            try:
                result.extend(self.arch_db.find(instruction, entry.cpuid))
            except KeyError:
                pass

        return result


def format_architecture(arch_code):
    from lib.uops import architecture_name

    return architecture_name(arch_code)


class Range(object):
    def __init__(self, val):
        self.start = val
        self.end   = val

    def __str__(self):
        if self.start != self.end:
            return '%d-%d' % (self.start, self.end)
        else:
            return '%d' % self.start


    __repr__ = __str__


def format_latency(latencies):
    if latencies is None:
        return '\-'

    if type(latencies) is int:
        return str(latencies)

    if len(latencies) == 1:
        for number in latencies:
            return str(number)

    result = []
    tmp    = sorted(latencies)
    r      = Range(tmp[0])
    for lat in tmp[1:]:
        if r.end + 1 == lat:
            r.end = lat
        else:
            result.append(r)
            r = Range(lat)

    result.append(r)

    return ', '.join(map(str, result))


def format_port_details(port_details):
    if port_details is None:
        return '\-'

    return ' '.join('p%s:%d' % (pd.ports, pd.uops) for pd in port_details)

