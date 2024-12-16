def architecture_name(arch_code):
    names = {
        "CON":   "Conroe",
        "WOL":   "Wolfdale",
        "NHM":   "Nehalem",
        "WSM":   "Westmere",
        "SNB":   "Sandy Bridge",
        "IVB":   "Ivy Bridge",
        "HSW":   "Haswell",
        "BDW":   "Broadwell",
        "SKL":   "Skylake",
        "SKX":   "Skylake-X",
        "KBL":   "Kaby Lake",
        "CFL":   "Coffee Lake",
        "CNL":   "Cannon Lake",
        "CLX":   "Cascade Lake",
        "ICL":   "Ice Lake",
        "TGL":   "Tiger Lake",
        "RKL":   "Rocket Lake",
        "ADL-P": "Alder Lake-P",
        "BNL":   "Bonnell",
        "AMT":   "Airmont",
        "GLM":   "Goldmont",
        "GLP":   "Goldmont Plus",
        "TRM":   "Tremont",
        "ADL-E": "Alder Lake-E",
        "ZEN+":  "AMD Zen+",
        "ZEN2":  "AMD Zen2",
        "ZEN3":  "AMD Zen3",
        "ZEN4":  "AMD Zen4",
    }

    return names.get(arch_code, arch_code)


def normalize(string):
    symbols = set(['CFL',
                   'SNM',
                   'SNB',
                   'KBL',
                   'IVB',
                   'NHM',
                   'SKX',
                   'BDW',
                   'HSW',
                   'SKL'])

    mapping = {
        'COFFEELAKE'    : 'CFL',
        'SANDYBRIDGE'   : 'SNB',
        'KABYLAKE'      : 'KBL',
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
        return mapping[tmp]
    except KeyError:
        if tmp in symbols:
            return tmp
        else:
            raise KeyError("'%s' is not a valid architecture name nor symbol" % string)

