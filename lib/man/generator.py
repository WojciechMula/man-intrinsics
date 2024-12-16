from .patterns import *
from os.path import join
from os.path import exists
from os.path import islink
from os.path import basename

import os
import gzip

import logging
log = logging.getLogger('main')

from .generator_base import GeneratorBase


class Generator(GeneratorBase):

    def generate(self):
        if True:
            log.info("Generating man pages in %s", self.options.target_dir)
            self.generate_man_pages()

        if self.options.create_symlinks:
            log.info("Creating links to man pages for CPU instructions")
            self.generate_links()


        return [basename(path) for path in self.created_files]


    def generate_man_pages(self):
        if self.options.gzip:
            def open_file(path):
                return gzip.open(path, 'wt')
        else:
            def open_file(path):
                return open(path, 'wt')

        for i, entry in enumerate(self.instr_db.entries):
            path = self.get_path(entry)

            log.debug("Generating %s (%d of %d)" % (path, i+1, len(self.instr_db)))

            text = self.generate_man_page(entry)
            with open_file(path) as f:
                f.write(unicode(text).encode('utf8'))
                self.created_files.append(path)


    def generate_man_page(self, entry):
        data = {}
        data['group']       = MAN_GROUP
        data['date']        = self.instr_db.date
        data['version']     = self.instr_db.version

        data['technology']  = entry.technology
        data['name']        = entry.name
        data['include']     = entry.include
        data['rettype']     = entry.rettype
        data['arguments']   = entry.arguments
        data['description'] = entry.description
        data['operation']   = entry.operation

        res = MAIN % data

        if not entry.instructions:
            res += NO_INSTRUCTION_NOTE

        if entry.categories:
            tmp = [CATEGORY_ENTRY % item for item in entry.categories]
            res += CATEGORY_HEADER % (', '.join(tmp))

        if entry.has_round_note:
            res += ROUND_NOTE

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
            for flag in sorted(entry.cpuid):
                tmp = {
                    'flag': flag,
                    'last': '',
                }
                res += CPUID_ENTRY % tmp

        res += self.generate_arch_details(entry)
        res += self.generate_see_also(entry)

        return res


    def generate_links(self):
        for instruction, entries in self.by_instruction.iteritems():
            target = self.get_linkpath(instruction)
            source = self.get_filename(entries[0])
            if exists(target):
                if islink(target):
                    os.unlink(target)
                else:
                    raise RuntimeError("'%s' already exists and is not a symlink" % target)

            os.symlink(source, target)
            self.created_files.append(target)


    def get_linkpath(self, instruction):
        path = join(self.options.target_dir, instruction) + '.' + MAN_GROUP
        if self.options.gzip:
            path += '.gz'

        return path


    def get_filename(self, entry):
        name = '%s.%s' % (entry.unique_name, MAN_GROUP)
        if self.options.gzip:
            name += '.gz'

        return name


    def get_path(self, entry):
        return join(self.options.target_dir, self.get_filename(entry))


