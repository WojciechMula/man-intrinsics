#!/usr/bin/env python
import textwrap


def main():
    options = get_options()
    app = Application(options)
    app.run()


def fmtlist(list):
    return ', '.join(list)


def fmtset(set):
    return ', '.join(sorted(set))


class DataSource(object):
    def __init__(self, options):
        self.options = options
        self.instructions = None
        self.architecture = None
        self.filter_by_isa  = get_filter_by_isa(options)
        self.filter_by_arch = get_filter_by_arch(options)


    def get_instructions(self):
        if self.instructions is None:
            from lib.guide.loader import load

            opts = self.options

            path = opts.instructions_xml
            print "Loading instructions from %s" % path
            if opts.enabled_instruction_sets:
                print "- will include only ISA(s): %s" % fmtset(opts.enabled_instruction_sets)
            if self.options.disabled_instruction_sets:
                print "- will exclude ISA(s): %s" % fmtset(opts.disabled_instruction_sets)

            self.instructions = load(path, self.filter_by_isa)

        return self.instructions


    def get_architecture_details(self):
        if self.architecture is None and self.options.uops_xml is not None:
            from lib.uops.loader import load
            from lib.uops import architecture_name

            opts = self.options

            path = opts.uops_xml
            print "Loading architecture details from %s" % path
            if opts.enabled_architectures:
                tmp = map(architecture_name, opts.enabled_architectures)
                print "- will include only architecture(s): %s" % fmtset(tmp)
            if opts.disabled_architectures:
                tmp = map(architecture_name, opts.disabled_architectures)
                print "- will exclude architecture(s): %s" % fmtset(tmp)

            def silent(s):
                pass
            self.architecture = load(path, silent)

        return self.architecture


class Application(object):
    def __init__(self, options):
        self.options = options
        self.datasource = DataSource(options)


    def run(self):
        from lib.man.generate import Generator

        if self.options.dump_isa or self.options.dump_arch:
            if self.options.dump_isa:
                self.dump_isa()

            if self.options.dump_arch:
                self.dump_arch()
        else:
            gen = Generator(self.options, self.datasource)
            gen.generate()


    def dump_isa(self):
        instr_db = self.datasource.get_instructions()
        text = "List of ISAs defined in %s: %s." % \
               (self.options.instructions_xml, fmtset(instr_db.get_cpuids()))

        print '\n'.join(textwrap.wrap(text))


    def dump_arch(self):
        from lib.uops import architecture_name

        arch_db = self.datasource.get_architecture_details()

        print "List of architectures defined in %s" % self.options.uops_xml
        for symbol in sorted(arch_db.get_architectures()):
            name = architecture_name(symbol)
            if name != symbol:
                print '* %s (%s)' % (name, symbol)
            else:
                print '* %s' % symbol


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

    return options


def get_filter_by_isa(options):

    enabled = options.enabled_instruction_sets
    disabled = options.disabled_instruction_sets

    if len(enabled) > 0 and len(disabled) > 0:
        def filter(cpuids):
            return bool(cpuids & enabled) and not bool(cpuids & disabled)
    elif len(enabled) > 0:
        def filter(cpuids):
            return bool(cpuids & enabled)
    elif len(disabled) > 0:
        def filter(cpuids):
            return not bool(cpuids & disabled)
    else:
        def filter(_):
            return True

    return filter


def get_filter_by_arch(options):
    from lib.uops import normalize

    enabled  = set((normalize(name_or_symbol) for name_or_symbol in options.enabled_architectures))
    disabled = set((normalize(name_or_symbol) for name_or_symbol in options.disabled_architectures))

    if len(enabled) > 0 and len(disabled) > 0:
        def filter(arch_symbol):
            return arch_symbol in enabled and arch_symbol not in disabled
    elif len(enabled) > 0:
        def filter(arch_symbol):
            return arch_symbol in enabled
    elif len(disabled) > 0:
        def filter(arch_symbol):
            return arch_symbol not in disabled
    else:
        def filter(_):
            return True

    return filter


if __name__ == '__main__':
    main()
