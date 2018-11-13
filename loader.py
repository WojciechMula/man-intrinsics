import xml.etree.ElementTree as ET

class Entry(object):
    def __init__(self):
        pass


class Builder(object):
    def __init__(self, intrinsic):
        assert intrinsic.tag == 'intrinsic'
        self.intrinsic = intrinsic

        self.children = {}
        self.parameters = []
        self.instructions = []
        self.types = []
        self.cpuid = []
        for child in intrinsic:
            if child.tag == 'parameter':
                self.parameters.append(child)
            elif child.tag == 'instruction':
                self.instructions.append(child)
            elif child.tag == 'type':
                self.types.append(child)
            elif child.tag == 'CPUID':
                self.cpuid.append(child)
            else:
                self.children[child.tag] = child

    def build(self):
        e = Entry()
        e.name          = self.intrinsic.attrib['name']
        e.technology    = self.intrinsic.attrib['tech']

        tmp = self.children['description'].text
        round_note_tag = '[round_note]'
        if round_note_tag in tmp:
            tmp = tmp.replace(round_note_tag, '')
            e.has_round_note = True
        else:
            e.has_round_note = False

        e.description   = normalize(tmp)

        # merge category and types --- it's an arbitrary Intel's classification, not that important
        e.categories    = [self.children['category'].text]
        for item in self.types:
            e.categories.append(item.text)

        e.categories.sort()

        try:
            e.operation = self.children['operation'].text.strip()
        except KeyError:
            e.operation = None

        e.include       = self.children['header'].text
        e.rettype       = self.intrinsic.attrib['rettype']

        try:
            e.instructions = []
            for instr in self.instructions:
                name = instr.attrib['name'].lower()
                form = instr.attrib['form']
                e.instructions.append((name, form))

        except KeyError:
            e.instructions = []

        e.cpuid = [item.text for item in self.cpuid]
        e.cpuid.sort()

        tmp = ['%s %s' % (item.attrib['type'], item.attrib['varname']) for item in self.parameters]
        e.arguments = ', '.join(tmp)
        if e.arguments == 'void ':
            e.arguments = ''

        return e


def normalize(s):
    tmp = s.split()
    return ' '.join(tmp)


def load(path):
    data = ET.parse(path)
    entries = []
    date    = None
    version = None
    for item in data.iter():
        if item.tag == 'intrinsics_list':
            date    = item.attrib['date']
            version = item.attrib['version']
            break

    assert date is not None

    for intrinsic in data.getroot():
        #print intrinsic.attrib

        b = Builder(intrinsic)
        entries.append(b.build())

    return date, version, entries


