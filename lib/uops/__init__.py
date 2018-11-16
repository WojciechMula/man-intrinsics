def architecture_name(arch_code):
    names = {
        #'CFL': '',
        #'SNM': '',
        #'SNB': '',
        #'KBL': '',
        'IVB': 'Ivy Bridge',
        'NHM': 'Nehalem',
        'WSM': 'Westmere',
        'SKX': 'SkylakeX',
        'BDW': 'Broadwell',
        'HSW': 'Haswell',
        'SKL': 'Skylake',
    }

    return names.get(arch_code, arch_code)


def normalize_arch_code(string):
    symbols = set('CFL',
                'SNM',
                'SNB',
                'KBL',
                'IVB',
                'NHM',
                'SKX',
                'BDW',
                'HSW',
                'SKL')

    mapping = {
        'IVY BRIDGE'    : 'IVB',
        'IVYBRIDGE'     : 'IVB',
        'NEHALEM'       : 'NHM',
        'WESTMERE'      : 'WSM',
        'SKYLAKEX'      : 'SKX',
        'BROADWELL'     : 'BDW',
        'HASWELL'       : 'HSW',
        'SKYLAKE'       : 'SKL',
    }

    tmp = string.upper()

    try:
        return mapping(tmp)
    except KeyError:
        if tmp in symbols:
            return tmp
        else:
            raise KeyError("'%s' is not a valid architecture name nor symbol" % string)

