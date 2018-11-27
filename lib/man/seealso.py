from seealso_patterns import *
from patterns import MAN_GROUP


class Struct(object):
    pass


class Generate(object):
    def __init__(self, by_instruction, duplicated_names):
        self.by_instruction = by_instruction
        self.duplicated_names = duplicated_names


    def generate(self, entry):
        see_also = self.see_also(entry)
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


    def see_also(self, entry):
        s = Struct()
        s.list = []

        def get_entries(instruction):
            try:
                s.list.extend(self.by_instruction[instruction])
            except KeyError:
                pass

        try:
            for item in self.duplicated_names[entry.name]:
                if entry.unique_name != item.unique_name:
                    s.list.append(item)
        except KeyError:
            pass


        for instr, _ in entry.instructions:
            get_entries(instr)

            if instr.startswith('p') or instr.startswith('vp'):
                # integer instructions

                get_entries('vp' + instr[1:]) # try match pshufb [SSE] with vpshufb [AVX]
                get_entries('v'  + instr[2:]) # or vice-versa

            elif instr.endswith('ps') or instr.endswith('pd') or instr.endswith('ss'):
                # floating point instructions
                get_entries(instr[:-2] + 'pd') # addXX -> addpd
                get_entries(instr[:-2] + 'ps') # addXX -> addpd
                get_entries(instr[:-2] + 'ss') # addXX -> addss

                if instr.startswith('v'):
                    get_entries(instr[1:-2] + 'pd') # vaddXX -> addpd
                    get_entries(instr[1:-2] + 'ps') # vaddXX -> addpd
                    get_entries(instr[1:-2] + 'ss') # vaddXX -> addss
                else:
                    get_entries('v' + instr[:-2] + 'pd') # addXX -> vaddpd
                    get_entries('v' + instr[:-2] + 'ps') # addXX -> vaddpd
                    get_entries('v' + instr[:-2] + 'ss') # addXX -> vaddss


        if len(s.list) <= 1:
            return

        list = sorted(set(s.list))

        return [item.name for item in list if item.name != entry.name]
