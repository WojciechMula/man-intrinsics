class Entry(object):
    __slots__ = (
        'name',
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

    def __init__(self):
        pass


class Database(object):
    def __init__(self):
        self.date    = None
        self.version = None
        self.entries = []


    def __len__(self):
        return len(self.entries)

