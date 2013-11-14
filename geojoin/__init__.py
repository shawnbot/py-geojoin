# import sys

def get_key_limiter(props, key_prefix=None):
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
    apply_props = get_prop_setter(mode, props, fk=feature_fk, key_prefix=key_prefix)

    rows_by_key = {}
    for row in rows:
        key = row.get(data_fk)
        rows_by_key[key] = row

    row_keys = set(rows_by_key.keys())
    # print >> sys.stderr, '%d row keys' % len(row_keys)

    feature_keys = set(map(lambda f: str(f['properties'].get(feature_fk)), features))
    # print >> sys.stderr, '%d feature keys' % len(feature_keys)

    common_keys = row_keys.intersection(feature_keys)
    # print >> sys.stderr, '%d keys in common' % len(common_keys)

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
