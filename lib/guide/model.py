class Entry(object):
    __slots__ = (
        'name',
        'unique_name',
        'rettype',
        'include',
        'description',
        'categories',
        'operation',
        'technology',
        'instructions',
        'arguments',
        'cpuid',
        'has_round_note',
    )


class Database(object):
    def __init__(self):
        self.date    = None
        self.version = None
        self.entries = []


    def get_cpuids(self):
        result = set()
        for instr in self.entries:
            result.update(instr.cpuid)

        return result


    def __len__(self):
        return len(self.entries)

