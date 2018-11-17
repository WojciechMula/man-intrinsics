import os
import errno
import textwrap
import logging

from patterns import *

log = logging.getLogger('main')


class DebSupport(object):
    def __init__(self, options, datasource):
        self.options = options
        self.datasource = datasource


    def create(self):
        self.dir = os.path.join(self.options.deb_dir, 'DEBIAN')
        try:
            os.mkdir(self.dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        self.create_control()
        self.create_postinst()
        self.create_postrm()


    def create_control(self):
        path = os.path.join(self.dir, 'control')
        with open(path, 'wt') as f:
            version, details = self.__prepare_control_parameters()
            data = {
                'version'    : version,
                'details'    : details,
                'maintainer' : os.getlogin(),
            }

            content = CONTROL % data
            f.write(content)

            log.info("%s was created" % path)


    def __prepare_control_parameters(self):
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

            from lib.uops import normalize
            if len(self.options.enabled_architectures) > 0:
                tmp = set((normalize(name_or_symbol) for name_or_symbol in self.options.enabled_architectures))
                arch += " Included architectures: %s." % fmtset(tmp)

            if len(self.options.disabled_architectures) > 0:
                tmp = set((normalize(name_or_symbol) for name_or_symbol in self.options.enabled_architectures))
                arch += " Excluded architectures: %s." % fmtset(tmp)

            details.append('.') # FIXME: seems '.' is the line separator
            details.extend(textwrap.wrap(arch))

        # important: description has to be indented
        details = '\n'.join(' ' + line for line in details)

        return (instr_db.version, details)


    def _create_script(self, name, content):
        path = os.path.join(self.dir, name)
        if os.path.exists(path):
            os.unlink(path)

        with open(path, 'wt') as f:
            f.write(content)

        os.chmod(path, 0555) # read/execute

        log.info("%s was created" % path)


    def create_postinst(self):
        self._create_script('postinst', POSTINST)


    def create_postrm(self):
        self._create_script('postrm', POSTREMOVE)


def fmtset(set):
    return ', '.join(sorted(set))
