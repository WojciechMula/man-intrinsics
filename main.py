#!/usr/bin/env python

def main():
    options = get_options()
    app = Application(options)
    app.run()


class DataSource(object):
    def __init__(self, options):
        self.options = options
        self.instructions = None
        self.architecture = None


    def get_instructions(self):
        if self.instructions is None:
            from lib.guide.loader import load

            path = self.options.instructions_xml
            print "Loading instructions from %s" % path
            self.instructions = load(path)

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

        if self.options.dump_isa or self.options.dump_arch:
            raise NotImplementedError()
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

    parser.add_option('-u', '--uops', dest='uops_xml', metavar='XML',
        help="path to .xml from uops.info [otional]"
    )

    parser.add_option('--dump-isa', action='store_true', default=False,
        help="list available ISAs and exit"
    )

    parser.add_option('--isa', dest='enabled_instruction_sets', action='append', metavar='NAME',
        help="generate manual pages for given instruction set (can be passed many times)"
    )

    parser.add_option('--omit-isa', dest='disabled_instruction_sets', action='append', metavar='NAME',
        help="do not generate manual only for given instruction set (can be passed many times)"
    )


    parser.add_option('--dump-arch', action='store_true', default=False,
        help="list available archs and exit"
    )
    parser.add_option('--arch', dest='enabled_architectures', action='append', metavar='NAME',
        help="include instruction timings for given architecture (can be passed many times)"
    )

    parser.add_option('--omit-arch', dest='disabled_architectures', action='append', metavar='NAME',
        help="do not include instruction timings for given architecture (can be passed many times)"
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

    if options.target_dir is None:
        raise parser.error('--output is required')

    if options.dump_arch or \
       (options.enabled_architectures is not None) or \
       (options.enabled_architectures is not None):

        raise parser.error('--uarch is required when --dump-arch, --arch or --omit-arch is used')

    return options


if __name__ == '__main__':
    main()
