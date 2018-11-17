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


    def get_instructions(self):
        if self.instructions is None:
            from lib.guide.loader import load

            opts = self.options

            path = opts.instructions_xml
            print "Loading instructions from %s" % path
            if opts.enabled_instruction_sets:
                print "- will include only ISAs: %s" % fmtlist(opts.enabled_instruction_sets)
            if self.options.disabled_instruction_sets:
                print "- will exclude ISAs: %s" % fmtlist(opts.disabled_instruction_sets)

            self.instructions = load(path, get_filter_by_isa(opts))

        return self.instructions


    def get_architecture_details(self):
        if self.architecture is None and self.options.uops_xml is not None:
            from lib.uops.loader import load

            path = self.options.uops_xml
            print "Loading architecture details from %s" % path

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

        if self.options.dump_isa:
            instr_db = self.datasource.get_instructions()
            text = "List of ISAs defined in %s: %s." % \
                   (self.options.instructions_xml, fmtset(instr_db.get_cpuids()))

            print '\n'.join(textwrap.wrap(text))
        else:
            gen = Generator(self.options, self.datasource)
            gen.generate()


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

    parser.add_option('-l', '--create-symlinks', dest='create_symlinks', action='store_true', default=False,
        help="create symbolic links between intrinsics functions and CPU instructions"
    )

    parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False,
        help="be verbose"
    )

    options, _ = parser.parse_args()
    if options.instructions_xml is None:
        raise parser.error('--guide is required')

    if options.target_dir is None and \
       not options.dump_isa:
        raise parser.error('--output is required')

    if options.dump_isa:
        options.enabled_instruction_sets = set()
        options.disabled_instruction_sets = set()
    else:
        options.enabled_instruction_sets = set(options.enabled_instruction_sets)
        options.disabled_instruction_sets = set(options.disabled_instruction_sets)

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


if __name__ == '__main__':
    main()
