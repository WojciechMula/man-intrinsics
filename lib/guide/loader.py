import xml.etree.ElementTree as ET
import logging

log = logging.getLogger('main')

from .model import *


class Builder(object):
    def __init__(self, intrinsic, filter_by_isa):
        assert intrinsic.tag == 'intrinsic'
        self.intrinsic = intrinsic
        self.filter_by_isa = filter_by_isa

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

        e.name       = self.intrinsic.attrib['name']
        e.technology = self.intrinsic.attrib['tech']

        e.cpuid = []
        for item in self.cpuid:
            tmp = item.text.split('/')
            e.cpuid.extend(tmp)

        e.cpuid = set(e.cpuid)
        if not self.filter_by_isa(e.cpuid):
            return None

        tmp = self.children['description'].text
        round_note_tag = '[round_note]'
        if round_note_tag in tmp:
            tmp = tmp.replace(round_note_tag, '')
            e.has_round_note = True
        else:
            e.has_round_note = False

        e.description = normalize_text(tmp)

        # merge category and types --- it's an arbitrary Intel's classification, not that important
        e.categories = [self.children['category'].text]
        for item in self.types:
            e.categories.append(item.text)

        e.categories.sort()

        try:
            e.operation = self.children['operation'].text.strip()
        except KeyError:
            e.operation = None

        e.include = self.children['header'].text
        e.rettype = self.children['return'].attrib['type']

        e.instructions = []
        for instr in self.instructions:
            name = instr.attrib['name'].lower()
            form = instr.attrib.get('form', '') # might not be present
            e.instructions.append((name, form))

        tmp = ['%s %s' % (item.attrib['type'], item.attrib.get('varname', ''))
               for item in self.parameters]
        e.arguments = ', '.join(tmp)
        if e.arguments == 'void ': # that's silly
            e.arguments = ''

        return e


def normalize_text(s):
    tmp = s.split()
    return ' '.join(tmp)


def normalize_date(mdy_date):
    m, d, y = mdy_date.split('/')

    return '%s-%s-%s' % (y, m, d)


def load(path, filter_by_isa):
    log.debug("Loading data from %s", path)
    data = ET.parse(path)

    db = Database()

    item = next(data.iter('intrinsics_list'))
    db.date    = normalize_date(item.attrib['date'])
    db.version = item.attrib['version']

    log.debug("Parsing instructions")
    for intrinsic in data.getroot():
        log.debug("parsing %s", intrinsic.attrib['name'])
        b = Builder(intrinsic, filter_by_isa)
        entry = b.build()
        if entry:
            db.entries.append(entry)

    return db
