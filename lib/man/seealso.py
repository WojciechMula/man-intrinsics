from .seealso_patterns import *
from .patterns import MAN_GROUP


class Generate(object):
    def __init__(self, by_instruction, duplicated_names):
        self.by_instruction = by_instruction
        self.duplicated_names = duplicated_names


    def generate(self, entry):
        p = Finder(entry, self.by_instruction, self.duplicated_names)
        see_also = p.find()
        if not see_also:
            return ''

        res = SEE_ALSO_HEADER
        for i, name in enumerate(see_also):
            if i + 1 < len(see_also):
                last = ','
            else:
                last = ''

            data = {
                'name'  : name,
                'group' : MAN_GROUP,
                'last'  : last
            }
            res += SEE_ALSO_ENTRY % data

        return res


class Finder(object):
    def __init__(self, entry, by_instruction, duplicated_names):

        self.by_instruction = by_instruction
        self.duplicated_names = duplicated_names
        self.entry = entry
        self.list  = []


    def find(self):
        self.find_duplicates()
        self.find_by_instruction()

        if len(self.list) <= 1:
            return

        list = sorted(set(self.list))

        return [entry.unique_name for entry in list if entry.unique_name != self.entry.unique_name]


    def find_duplicates(self):
        try:
            dups = self.duplicated_names[self.entry.name]
        except KeyError:
            return

        for entry in dups:
            if entry.unique_name != self.entry.unique_name:
                self.list.append(entry)


    def find_by_instruction(self):
        for instruction in self.__get_instructions():
            try:
                self.list.extend(self.by_instruction[instruction])
            except KeyError:
                pass


    def __get_instructions(self):
        for instruction, _ in self.entry.instructions:
            yield instruction
            for similar in self.__similar_instructions(instruction):
                yield similar


    def __similar_instructions(self, instr):

        if instr.startswith('p') or instr.startswith('vp'):
            # integer instructions
            yield 'vp' + instr[1:] # try match pshufb [SSE] with vpshufb [AVX]
            yield 'v'  + instr[2:] # or vice-versa

        elif instr.endswith('ps') or instr.endswith('pd') or instr.endswith('ss'):
            # floating point instructions
            yield instr[:-2] + 'pd' # addXX -> addpd
            yield instr[:-2] + 'ps' # addXX -> addpd
            yield instr[:-2] + 'ss' # addXX -> addss

            if instr.startswith('v'):
                yield instr[1:-2] + 'pd' # vaddXX -> addpd
                yield instr[1:-2] + 'ps' # vaddXX -> addpd
                yield instr[1:-2] + 'ss' # vaddXX -> addss
            else:
                yield 'v' + instr[:-2] + 'pd' # addXX -> vaddpd
                yield 'v' + instr[:-2] + 'ps' # addXX -> vaddpd
                yield 'v' + instr[:-2] + 'ss' # addXX -> vaddss


