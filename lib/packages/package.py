import textwrap

class Package(object):
    def __init__(self, options, datasource):
        self.options = options
        self.datasource = datasource


    def format_version(self):
        instr_db = self.datasource.get_instructions()

        return instr_db.version

    
    def get_description(self):
        details = []

        instr_db = self.datasource.get_instructions()
        guide = "Instruction descriptions from Intel Intrinsics Guide: version %s, data %s." % \
                 (instr_db.version, instr_db.date)

        if len(self.options.enabled_instruction_sets) > 0:
            guide += " Included ISAs: %s." % fmtset(self.options.enabled_instruction_sets)

        if len(self.options.disabled_instruction_sets) > 0:
            guide += " Excluded ISAs: %s." % fmtset(self.options.disabled_instruction_sets)

        details.extend(textwrap.wrap(guide))

        if self.datasource.include_architecture_details():
            metadata = self.datasource.get_uopos_metadata()
            arch = "Instruction architecture details from uops.info, file SHA-1 %s." % (metadata.sha512)

            if len(self.options.enabled_architectures) > 0:
                tmp = set((normalize(name_or_symbol) for name_or_symbol in self.options.enabled_architectures))
                arch += " Included architectures: %s." % fmtset(tmp)

            if len(self.options.disabled_architectures) > 0:
                tmp = set((normalize(name_or_symbol) for name_or_symbol in self.options.enabled_architectures))
                arch += " Excluded architectures: %s." % fmtset(tmp)

            details.append('')
            details.extend(textwrap.wrap(arch))

        return details


    def format_description(self):
        return '\n'.join(self.get_description())


def fmtset(set):
    return ', '.join(sorted(set))

