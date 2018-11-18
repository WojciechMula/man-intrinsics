import xml.etree.ElementTree as ET
import sys
import logging

log = logging.getLogger('main')

from model import *
from db import *

def load(path):
    log.debug("Loading data from '%s'...", path)
    data = ET.parse(path)

    log.debug("Processing instructions...")
    instructions = []
    for instruction in data.getroot().getiterator('instruction'):
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

    return InstructionsDB(instructions)


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
    for architecture in instruction.getiterator('architecture'):
        name = architecture.attrib['name']
        measurements = parse_measurements(architecture)
        if measurements:
            tmp[name] = measurements

    data.measurements = tmp

    return data


def parse_measurements(architecture):
    result = []
    # we favour real-world measurements over IACA results
    for item in architecture.getiterator('measurement'):
        result.append(parse_measurement(item))

    if not result:
        # if the worst cames to true, we pick the latest IACA
        iaca = None
        for item in architecture.getiterator('IACA'):
            tmp = parse_iaca(item)
            if iaca is None or tmp.version > iaca.version:
                iaca = tmp

        if iaca:
            result = [iaca]

    return result


def parse_measurement(measurement):
    data = Measurement()
    data.throughput   = optional_float(measurement.attrib, 'throughput')
    data.total_uops   = int(measurement.attrib['total_uops'])
    data.uops_details = parse_ports(measurement)

    # we're not dig into latency conditions, just record cycles
    tmp = set()
    for latency in measurement.getiterator('latency'):
        try:
            cycles = int(latency.attrib['cycles'])
            tmp.add(cycles)
        except KeyError:
            min = int(latency.attrib['minCycles'])
            max = int(latency.attrib['maxCycles'])
            for cycles in range(min, max+1):
                tmp.add(cycles)

    if tmp:
        data.latency = tuple(sorted(tmp))

    return data


def parse_iaca(iaca):
    data = IACAMeasurements()
    data.version      = float(iaca.attrib['version'])
    data.latency      = optional_int(iaca.attrib, 'latency')
    data.throughput   = optional_float(iaca.attrib, 'throughput')
    data.total_uops   = int(iaca.attrib['total_uops'])
    data.uops_details = parse_ports(iaca)

    return data




def parse_ports(tag):
    l = []
    for attr, value in tag.attrib.iteritems():
        if not attr.startswith('port'):
            continue

        d = PortDetail()
        d.ports = attr[4:]
        d.uops  = int(value)
        l.append(d)

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

