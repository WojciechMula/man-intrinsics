from patterns import *
from os.path import join
from os.path import exists
import codecs


class Generator(object):
    def __init__(self, date, version, entries):
        self.date    = date
        self.version = version
        self.entries = entries
        self.by_instruction = {}
        for entry in self.entries:
            if entry.instructions is None:
                continue

            for instr, _ in entry.instructions:
                if instr not in self.by_instruction:
                    self.by_instruction[instr] = [entry]
                else:
                    self.by_instruction[instr].append(entry)


    def generate(self, targetdir):
        for i, entry in enumerate(self.entries):
            path = join(targetdir, entry.name) + '.' + MAN_GROUP
            if exists(path):
                #raise RuntimeError("'%s' already exists, won't continue" % path)
                pass

            print("Generating %s (%d of %d)" % (path, i+1, len(self.entries)))
            text = self.generate_entry(entry)
            with codecs.open(path, 'wt', encoding='utf-8') as f:
                f.write(text)
        else:
            print("Done")


    def generate_entry(self, entry):
        data = {}
        data['group']       = MAN_GROUP
        data['date']        = self.date
        data['version']     = self.version

        data['technology']  = entry.technology
        data['name']        = entry.name
        data['include']     = entry.include
        data['rettype']     = entry.rettype
        data['arguments']   = entry.arguments
        data['description'] = entry.description
        data['operation']   = entry.operation
        data['category']    = entry.category
        data['type']        = entry.type

        res = MAIN % data

        if not entry.instructions:
            res += NO_INSTRUCTION_NOTE

        if entry.category is not None and entry.type is not None:
            res += CATEGORY_AND_TYPE % data
        elif entry.category is not None: 
            res += CATEGORY % data
            
        if entry.operation is not None:
            res += OPERATION % data

        if entry.instructions:
            res += INSTRUCTION_HEADER
            for instr, args in entry.instructions:
                tmp = {
                    'instruction': instr,
                    'arguments'  : args,
                }
                res += INSTRUCTION_ENTRY % tmp
            res += INSTRUCTION_TAIL

        if entry.cpuid:
            res += CPUID_HEADER
            for flag in entry.cpuid:
                tmp = {
                    'flag': flag,
                    'last': '',
                }
                res += CPUID_ENTRY % tmp

        see_also = self.see_also(entry)
        if see_also:
            res += SEE_ALSO_HEADER
            for i, name in enumerate(see_also):
                if i + 1 < len(see_also):
                    last = ','
                else:
                    last = ''

                tmp = {'name': name, 'group': MAN_GROUP, 'last': last}
                res += SEE_ALSO_ENTRY % tmp

        return res


    def see_also(self, entry):
        list = []
        for instr, _ in entry.instructions:
            try:
                list.extend(self.by_instruction[instr])
            except KeyError:
                return

        if len(list) <= 1:
            return

        return [item.name for item in sorted(list) if item.name != entry.name]

