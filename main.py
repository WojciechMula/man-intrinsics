#!/usr/bin/env python3
import textwrap
import logging
log = logging.getLogger('main')

from lib.packages.deb import create_files as create_deb_files
from lib.packages.rpm import create_spec_file
from lib.datasource import DataSource


def main():
    options = get_options()
    app = Application(options)
    app.run()


def fmtset(set):
    return ', '.join(sorted(set))


class Application(object):
    def __init__(self, options):
        self.options = options
        self.datasource = DataSource(options)


    def run(self):
        from lib.man.generator import Generator

        if self.options.dump_isa or self.options.dump_arch:
            if self.options.dump_isa:
                self.dump_isa()

            if self.options.dump_arch:
                self.dump_arch()
        else:
            gen = Generator(self.options, self.datasource)
            generated_files = gen.generate()

            if self.options.deb_dir is not None:
                create_deb_files(self.options, self.datasource)

            if self.options.rpm_spec_dir:
                create_spec_file(self.options, self.datasource, generated_files)


    def dump_isa(self):
        instr_db = self.datasource.get_instructions()
        text = "List of ISAs defined in %s: %s." % \
               (self.options.instructions_xml, fmtset(instr_db.get_cpuids()))

        print('\n'.join(textwrap.wrap(text)))


    def dump_arch(self):
        from lib.uops import architecture_name

        arch_db = self.datasource.get_architecture_details()

        print("List of architectures defined in %s" % self.options.uops_xml)
        for symbol in sorted(arch_db.get_architectures()):
            name = architecture_name(symbol)
            if name != symbol:
                print('* %s (%s)' % (name, symbol))
            else:
                print('* %s' % symbol)


def get_options():
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option('-o', '--output', dest='target_dir', metavar='DIR',
        help="path to output directory"
    )

    parser.add_option('-g', '--guide', dest='instructions_xml', metavar='XML',
        help="path to .xml from Intrinsic Guide [required]"
    )

    parser.add_option('--dump-isa', action='store_true', default=False,
        help="list available ISAs and exit"
    )

    parser.add_option('--isa', dest='enabled_instruction_sets', action='append', default=[], metavar='NAME',
        help="generate manual pages for given instruction set (can be passed many times)"
    )

    parser.add_option('--omit-isa', dest='disabled_instruction_sets', action='append', default=[], metavar='NAME',
        help="do not generate manual only for given instruction set (can be passed many times)"
    )


    parser.add_option('-u', '--uops', dest='uops_xml', metavar='XML',
        help="path to .xml from uops.info [otional]"
    )

    parser.add_option('--uops-no-ports', dest='uops_ports', action='store_false', default=True,
        help="do not include port allocation info"
    )

    parser.add_option('--dump-arch', action='store_true', default=False,
        help="list available archs and exit"
    )
    parser.add_option('--arch', dest='enabled_architectures', action='append', default=[], metavar='NAME',
        help="include instruction timings for given architecture (can be passed many times)"
    )

    parser.add_option('--omit-arch', dest='disabled_architectures', action='append', default=[], metavar='NAME',
        help="do not include instruction timings for given architecture (can be passed many times)"
    )

    parser.add_option('-l', '--create-symlinks', dest='create_symlinks', action='store_true', default=False,
        help="create symbolic links between intrinsics functions and CPU instructions"
    )

    parser.add_option('--deb', dest='deb_dir', default=None,
        help="create extra files required to build a .deb package (Debian, Ubuntu)"
    )

    parser.add_option('--rpm-spec-dir', dest='rpm_spec_dir', default=None,
        help="create a .spec file required to build an .rpm package (RedHat, Fedora)"
    )

    parser.add_option('--gzip', dest='gzip', action='store_true', default=False,
        help="gzip man pages"
    )

    parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False,
        help="be verbose"
    )


    options, _ = parser.parse_args()

    guide_required = True
    uops_required = False
    output_required = True
    if options.dump_arch and not options.dump_isa:
        guide_required = False

    if options.dump_arch:
        uops_required = True

    if options.dump_arch or options.dump_isa:
        output_required = False

    if guide_required and options.instructions_xml is None:
        raise parser.error('--guide is required')

    if uops_required and options.uops_xml is None:
        raise parser.error('--uops is required')

    if output_required and options.target_dir is None:
        raise parser.error('--output is required')

    if options.dump_isa:
        options.enabled_instruction_sets = set()
        options.disabled_instruction_sets = set()
    else:
        options.enabled_instruction_sets = set(options.enabled_instruction_sets)
        options.disabled_instruction_sets = set(options.disabled_instruction_sets)

    if options.dump_arch:
        options.enabled_architectures = set()
        options.disabled_architectures = set()
    else:
        options.enabled_architectures = set(options.enabled_architectures)
        options.disabled_architectures = set(options.disabled_architectures)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    if options.verbose:
        log.setLevel(logging.DEBUG)

    return options


if __name__ == '__main__':
    main()
