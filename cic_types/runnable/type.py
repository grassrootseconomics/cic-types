# standard imports
import argparse
import sys
import logging

# external imports
from cic_types.condiments import MetadataPointer
from cic_types.processor import (
        generate_metadata_pointer,
        phone_number_to_e164,
        )
from hexathon import strip_0x

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()


hextypes = [
        MetadataPointer.PERSON,
        MetadataPointer.CUSTOM,
        ]
e164types = [
        MetadataPointer.PHONE,
        ]

argparser = argparse.ArgumentParser()
argparser.add_argument('-t', '--type', dest='typ', help='Pointer type to generate')
argparser.add_argument('--list-types', dest='list', action='store_true', help='List all pointer types')
argparser.add_argument('-v', action='store_true', help='Verbose logging')
argparser.add_argument('value', nargs='?')
args = argparser.parse_args(sys.argv[1:])

if args.v:
    logg.setLevel(logging.DEBUG)

if args.list:
    for v in dir(MetadataPointer):
        if v[0] == '_':
            continue
        print(v.lower())
    sys.exit(0)

if args.value == None or args.typ == None:
    argparser.error('value and type are required\n')

p = None
try:
    p = getattr(MetadataPointer, args.typ.upper())
except AttributeError:
    sys.stderr.write('unknown metadata type {} (use --list-types for a list)\n'.format(args.typ))
    sys.exit(1)
logg.info('pointer type {}'.format(p))

v = args.value
vd = v
if p in hextypes:
    v = bytes.fromhex(strip_0x(v))
    vd = v.hex() + ' (bytes)'
elif p in e164types:
    v = phone_number_to_e164(v, None)
    vd = v
    v = v.encode('utf-8')
logg.info('interpreted value ' + vd)

print(generate_metadata_pointer(v, p))
