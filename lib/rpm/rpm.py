import os
import errno
import textwrap
import logging

from lib.uops import normalize

from patterns import *
log = logging.getLogger('main')


class RpmSupport(object):
    def __init__(self, options, datasource, generated_files):
        self.options = options
        self.datasource = datasource
        self.generated_files = generated_files


    def create(self):
        path = os.path.join(self.options.rpm_spec_dir, 'man-intrinsics.spec')
        with open(path, 'wt') as f:
            data = {
                'version'       : self.format_version(),
                'description'   : self.format_description(),
                'installdir'    : DEFAULT_DIR,
                'files'         : self.format_files(),
            }

            content = SPEC % data
            f.write(content)

            log.info("%s was created" % path)


    def format_version(self):

        instr_db = self.datasource.get_instructions()

        return instr_db.version


    def format_description(self):
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

        return '\n'.join(details)


    def format_files(self):
        result = []
        for name in self.generated_files:
            result.append(os.path.join(DEFAULT_DIR, name))

        return '\n'.join(result)


def fmtset(set):
    return ', '.join(sorted(set))
