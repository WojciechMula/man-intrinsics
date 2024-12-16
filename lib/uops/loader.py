import xml.etree.ElementTree as ET
import sys
import logging

log = logging.getLogger('main')

from .model import *
from .db import *

def load(path):
    log.debug("Loading data from '%s'...", path)
    data = ET.parse(path)

    log.debug("Processing instructions...")
    instructions = []
    root = data.getroot()
    date = root.attrib.get('date', '<unknown>')
    for instruction in root.iter('instruction'):
        cpuid = isa_to_cpuid(instruction.attrib['isa-set'])
        if cpuid is None:
            continue

        name = instruction.attrib['string']
        log.debug("parsing %s", name)
        instr = parse_instruction(instruction)
        if len(instr.measurements) > 0:
            instr.cpuid = cpuid
            instructions.append(instr)
        else:
            log.debug("no measurements for %s" % name)

    return InstructionsDB(instructions, date)


def isa_to_cpuid(isa_string):
    if isa_string.startswith('AVX512'):
        if isa_string.endswith('_128') or \
           isa_string.endswith('_256') or \
           isa_string.endswith('_128N'):

            # We skip AVX512_XXX_128{N} and AVX512_XXX_256
            # as these instruction cannot be generated
            # by intrinsics functions
            return

        for suffix in ['_512', '_KOP', '_SCALAR']:
            if isa_string.endswith(suffix):
                return isa_string[:-len(suffix)]

        return isa_string
    elif isa_string == 'PENTIUMMMX':
        return 'MMX'
    elif isa_string == 'SSE4':
        return 'SSE4.1'
    elif isa_string == 'SSE42':
        return 'SSE4.2'
    else:
        return isa_string


def parse_instruction(instruction):
    data = Instruction()
    data.name = instruction.attrib['asm'].lower()
    data.form = instruction.attrib['string'].lower()

    tmp = {}
    for architecture in instruction.iter('architecture'):
        name = architecture.attrib['name']
        measurements = parse_measurements(architecture)
        if measurements:
            tmp[name] = measurements

    data.measurements = tmp

    return data


def parse_measurements(architecture):
    result = []
    # we favour real-world measurements over IACA results
    for item in architecture.iter('measurement'):
        result.append(parse_measurement(item))

    if not result:
        # if the worst cames to true, we pick the latest IACA
        iaca = None
        for item in architecture.iter('IACA'):
            tmp = parse_iaca(item)
            if iaca is None or tmp.version > iaca.version:
                iaca = tmp

        if iaca:
            result = [iaca]

    return result


def parse_measurement(measurement):
    data = Measurement()
    data.throughput   = optional_float(measurement.attrib, 'TP_ports')
    data.total_uops   = int(measurement.attrib['uops'])
    data.uops_details = parse_ports(measurement)

    # we're not dig into latency conditions, just record cycles
    tmp = set()
    for latency in measurement.iter('latency'):
        if 'cycles' in latency.attrib:
            cycles = int(latency.attrib['cycles'])
            tmp.add(cycles)
        elif 'min_cycles' in latency.attrib and 'max_cycles' in latency.attrib:
            min = int(latency.attrib['min_cycles'])
            max = int(latency.attrib['max_cycles'])
            for cycles in range(min, max+1):
                tmp.add(cycles)

    if tmp:
        data.latency = tuple(sorted(tmp))

    return data


def parse_iaca(iaca):
    data = IACAMeasurements()
    data.version      = float(iaca.attrib['version'])
    data.latency      = optional_int(iaca.attrib, 'latency')
    data.throughput   = optional_float(iaca.attrib, 'TP')
    data.total_uops   = int(iaca.attrib['uops'])
    data.uops_details = parse_ports(iaca)

    return data


def parse_ports(tag):
    l = []
    try:
        ports_string = tag.attrib['ports']
    except KeyError:
        return tuple()

    # we have something like "1*p06+1*p23+1*p237+1*p4"
    for seq in ports_string.split('+'):
        uops, ports = seq.split('*')

        d = PortDetail()
        d.uops = int(uops)
        if ports.startswith('FP'):
            d.ports = ports[2:]
        elif ports.startswith('p'):
            d.ports = ports[1:]
        else:
            assert False, "unsupported syntax: %s" % ports

        l.append(d)

    for attr, value in tag.attrib.items():
        if not attr.startswith('port'):
            continue


    return tuple(l)


def optional_float(dict, key):
    try:
        return float(dict[key])
    except KeyError:
        pass


def optional_int(dict, key):
    try:
        return int(dict[key])
    except KeyError:
        pass

