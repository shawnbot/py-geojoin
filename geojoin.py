#!/usr/bin/env python
import sys, csv

def get_key_limiter(props, key_prefix=None):
    print >> sys.stderr, "get_key_limiter(): %s, %s" % (props, key_prefix)
    if props and len(props) > 0:
        if key_prefix:
            def limit_keys(src):
                return dict([('%s%s' % (key_prefix, k), src[k]) for k in src.keys() if k in props])
        else:
            def limit_keys(src):
                return dict([(k, src[k]) for k in src.keys() if k in props])
    elif key_prefix:
        def limit_keys(d):
            prefixed = {}
            for k in d.keys():
                prefixed[key_prefix + k] = d[k]
            return prefixed
    else:
        return lambda d: d
    return limit_keys

def get_prop_setter(mode, props, props_key="properties", fk="id", key_prefix=None):
    limit_keys = get_key_limiter(props, key_prefix)

    if mode == "replace":
        def apply_props(row, feature):
            feature[props_key] = limit_keys(row)
    elif mode == "merge":
        def apply_props(row, feature):
            updates = limit_keys(row)
            if updates.has_key(fk):
                del updates[fk]
            feature[props_key].update(updates)
    else:
        raise Exeception("unrecognized mode: %s" % mode)

    return apply_props

def join(rows, features, data_fk, feature_fk, mode="merge", props=None, key_prefix=None):
    print >> sys.stderr, "join(): %d features on %s:%s, mode=%s, props=%s, key_prefix=%s" \
        % (len(features), data_fk, feature_fk, mode, props, key_prefix)
    apply_props = get_prop_setter(mode, props, fk=feature_fk, key_prefix=key_prefix)

    rows_by_key = {}
    for row in rows:
        key = row.get(data_fk)
        rows_by_key[key] = row

    row_keys = set(rows_by_key.keys())
    print >> sys.stderr, '%d row keys' % len(row_keys)

    feature_keys = set(map(lambda f: str(f['properties'].get(feature_fk)), features))
    print >> sys.stderr, '%d feature keys' % len(feature_keys)

    common_keys = row_keys.intersection(feature_keys)
    print >> sys.stderr, '%d keys in common' % len(common_keys)

    valid_features = []
    for feature in features:
        key = str(feature['properties'].get(feature_fk))
        if key in common_keys:
            row = rows_by_key.get(key)
            apply_props(row, feature)
            valid_features.append(feature)
    return valid_features

def get_features(obj, topology_key=None):
    feature_type = obj.get("type")
    if feature_type == "Topology":
        if topology_key:
            return obj["objects"][topology_key]["geometries"]
        else:
            features = []
            for key, coll in obj["objects"].items():
                for geom in coll["geometries"]:
                    features.append(geom)
            return features
    elif feature_type == "FeatureCollection":
        return obj["features"]
    else:
        return [obj]

def set_features(obj, features, topology_key=None):
    feature_type = obj.get("type")
    if feature_type == "Topology":
        if not topology_key:
            raise "Need a key to set features in Topology collections"
        obj["objects"][topology_key]["geometries"] = features
    elif feature_type == "FeatureCollection":
        obj["features"] = features
    else:
        # nothing to see here
        pass

if __name__ == "__main__":
    import json, csv
    from optparse import OptionParser

    parser = OptionParser(usage='usage: %prog [options] csv json\n' """
    Merges data from a comma- (or tab-, pipe-, etc.) separated file into the
    properties of GeoJSON features by joining on a foreign key, and prints the
    resulting GeoJSON feature collection to stdout.""")
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
    features = get_features(collection)

    props = (options.props and options.props.split(',')) or None
    valid_features = join(
        csv_reader,
        features,
        data_fk=data_fk,
        feature_fk=feature_fk,
        mode=options.mode,
        props=props,
        key_prefix=options.key_prefix)

    print >> sys.stderr, "%d features" % len(features)
    print >> sys.stderr, str(features[0]['properties'])

    if options.only_valid:
        set_features(collection, features)

    indent = (options.pretty and 2) or None
    sep = (options.pretty and (', ', ': ')) or (',', ':')
    json.dump(collection, sys.stdout, indent=indent, separators=sep)
