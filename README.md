# geojoin

Merge CSV data into GeoJSON features!

To install via [pip](https://pypi.python.org/pypi/geojoin), just run:

```sh
$ [sudo] pip install geojoin
```

Or clone this repo and `[sudo] pip install .` from this directory. This should put an executable, `geojoin` into your path.

## Usage

```
Usage: geojoin [options] csv json

    Merges data from a comma- (or tab-, pipe-, etc.) separated file into the
    properties of GeoJSON (or TopoJSON) features by joining on a foreign key,
    and prints the resulting feature collection to stdout.

Options:
  -h, --help            show this help message and exit
  -f FK, --fk=FK        The CSV column and GeoJSON feature property name on
                        which to join. This may either be a single string, or
                        a colon-separated pair denoting the CSV column name
                        and GeoJSON feature property name, respectively. The
                        default is "id".
  -F FS, --field-separator=FS
                        The CSV file field separator, default: ,
  -q FQ, --field-quote=FQ
                        The CSV file field quote character, default: "
  -m MODE, --mode=MODE  
  -p PROPS, --props=PROPS
                        a comma-separated list of keys to merge or replace
  --prefix=KEY_PREFIX   The key prefix for merged or replaced keys
  -P, --pretty          Whether to pretty-print JSON (default: not pretty)
  --valid               Limit output to LIMIT features, useful for testing.
```
