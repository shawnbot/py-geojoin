#!/usr/bin/env python
import json, csv, sys
import geojoin

from optparse import OptionParser

parser = OptionParser(usage='usage: %prog [options] csv json\n' """
Merges data from a comma- (or tab-, pipe-, etc.) separated file into the
properties of GeoJSON (or TopoJSON) features by joining on a foreign key,
and prints the resulting feature collection to stdout.""")
parser.add_option('-f', '--fk', dest='fk', default='id',
                  help='The CSV column and GeoJSON feature property name on '
                       'which to join. This may either be a single string, or '
                       'a colon-separated pair denoting the CSV column name and '
                       'GeoJSON feature property name, respectively. The '
                       'default is "%default".')
parser.add_option('-F', '--field-separator', dest='fs', default=',',
    help='The CSV file field separator, default: %default')
parser.add_option('-q', '--field-quote', dest='fq', default='"',
    help='The CSV file field quote character, default: %default')
parser.add_option('-m', '--mode', dest='mode', default="merge")
parser.add_option('-p', '--props', dest='props', default='',
    help='a comma-separated list of keys to merge or replace')
parser.add_option('--prefix', dest='key_prefix',
    help="The key prefix for merged or replaced keys")
parser.add_option('-P', '--pretty', dest='pretty', action="store_true",
        help='Whether to pretty-print JSON (default: not pretty)')
parser.add_option('--valid', dest='only_valid', action="store_true",
    help='Limit output to LIMIT features, useful for testing.')

options, args = parser.parse_args()

if len(args) != 2:
    parser.print_help()
    sys.exit(1)

input_csv, input_json = args

if ':' in options.fk:
    data_fk, feature_fk = options.fk.split(':')
else:
    data_fk = feature_fk = options.fk

csv_reader = csv.DictReader(open(input_csv), delimiter=options.fs, quotechar=options.fq)
collection = json.load(open(input_json, 'r'))
features = geojoin.get_features(collection)

props = (options.props and options.props.split(',')) or None
valid_features = geojoin.join(
    csv_reader,
    features,
    data_fk=data_fk,
    feature_fk=feature_fk,
    mode=options.mode,
    props=props,
    key_prefix=options.key_prefix)

# print >> sys.stderr, "%d features" % len(features)
print >> sys.stderr, str(features[0]['properties'])

if options.only_valid:
    geojoin.set_features(collection, features)

indent = (options.pretty and 2) or None
sep = (options.pretty and (', ', ': ')) or (',', ':')
json.dump(collection, sys.stdout, indent=indent, separators=sep)
