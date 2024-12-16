from .uops import Generate as GenerateUopsDetails
from .seealso import Generate as GenerateSeeAlso


class GeneratorBase(object):
    def __init__(self, options, datasource):
        self.options = options
        self.datasource = datasource
        self.instr_db = datasource.get_instructions()
        self.created_files = []

        self.__create_instruction_lookup()
        self.__update_unique_names()
        self.__api_setup___arch()
        self.__api_setup___seealso()


    def __create_instruction_lookup(self):
        self.by_instruction = {}
        for entry in self.instr_db.entries:
            for instr, _ in entry.instructions:
                if instr not in self.by_instruction:
                    self.by_instruction[instr] = [entry]
                else:
                    self.by_instruction[instr].append(entry)


    def __update_unique_names(self):
        d = {}
        for entry in self.instr_db.entries:
            entry.unique_name = entry.name # most instructions do not repeat
            key = entry.name
            if key not in d:
                d[key] = []

            d[key].append(entry)

        self.duplicated_names = dict(((key, list) for key, list in d.iteritems() if len(list) > 1))

        # fixup duplicated names: append technology tag
        for name, list in self.duplicated_names.iteritems():
            for index, entry in enumerate(list):
                if index > 0:
                    entry.unique_name = '%s-%s' % (entry.unique_name, entry.technology.lower())


    def __api_setup___arch(self):
        if self.datasource.include_architecture_details():
            gen = GenerateUopsDetails(self.options, self.datasource)
            self.generate_arch_details = lambda entry: gen.generate(entry)
        else:
            self.generate_arch_details = lambda _: ''

        self.__update_unique_names()


    def __api_setup___seealso(self):
        gen = GenerateSeeAlso(self.by_instruction, self.duplicated_names)
        self.generate_see_also = lambda entry: gen.generate(entry)


