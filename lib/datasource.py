import logging
log = logging.getLogger('main')


from guide.loader import load as load_guide
from uops.loader import load as load_uops
from uops import architecture_name, normalize


class DataSource(object):
    def __init__(self, options):
        self.options = options
        self.instructions = None
        self.architecture = None
        self.filter_by_isa  = get_filter_by_isa(options)
        self.filter_by_arch = get_filter_by_arch(options)


    def get_instructions(self):
        if self.instructions is None:

            opts = self.options

            path = opts.instructions_xml
            log.info("Loading instructions from %s", path)
            if opts.enabled_instruction_sets:
                log.info("- will include only ISA(s): %s", fmtset(opts.enabled_instruction_sets))
            if self.options.disabled_instruction_sets:
                log.info("- will exclude ISA(s): %s", fmtset(opts.disabled_instruction_sets))

            self.instructions = load_guide(path, self.filter_by_isa)

        return self.instructions


    def include_architecture_details(self):
        return self.options.uops_xml is not None


    def get_architecture_details(self):
        if self.architecture is None and self.include_architecture_details():

            opts = self.options

            path = opts.uops_xml
            log.info("Loading architecture details from %s", path)
            if opts.enabled_architectures:
                tmp = map(architecture_name, opts.enabled_architectures)
                log.info("- will include only architecture(s): %s", fmtset(tmp))
            if opts.disabled_architectures:
                tmp = map(architecture_name, opts.disabled_architectures)
                log.info("- will exclude architecture(s): %s", fmtset(tmp))

            self.architecture = load_uops(path)

        return self.architecture


    def get_uopos_metadata(self):

        import hashlib

        def getsha512sum(path):
            h = hashlib.sha512()
            with open(path, 'rb') as f:
                h.update(f.read())

            return h.hexdigest()

        class Metadata(object):
            pass


        metadata = Metadata()
        metadata.filename = self.options.uops_xml
        metadata.sha512   = getsha512sum(metadata.filename)

        return metadata


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
