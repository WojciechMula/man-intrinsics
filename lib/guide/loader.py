import xml.etree.ElementTree as ET
from model import *


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

        e.instructions = []
        for instr in self.instructions:
            name = instr.attrib['name'].lower()
            form = instr.attrib.get('form', '') # might not be present
            e.instructions.append((name, form))

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

    db = Database()

    for item in data.iter():
        if item.tag == 'intrinsics_list':
            db.date    = item.attrib['date']
            db.version = item.attrib['version']
            break

    assert db.date is not None
    assert db.version is not None

    for intrinsic in data.getroot():
        b = Builder(intrinsic)
        db.entries.append(b.build())

    return db


