#!/usr/bin/env python

"""
Some json strings returned from internet doesn't quote the key, so json

simple will  not handle that correctly, demjson can do the job, so you can use
it like this:

python format_json.py json_file_name | python -mjson.tool

or read from stdin

cat json_file_name | python format_json.py | python -mjson.tool
"""

import sys

try:
    import demjson
except ImportError:
    sys.stderr.write("Can not import the demjson Python module.\n")
    sys.stderr.write("Try running:  easy_install demjson\n")
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_file = open(sys.argv[1])
    else:
        input_file = sys.stdin
    #input_file = sys.stdin

    json_str = input_file.read()
    print demjson.encode(demjson.decode(json_str), encoding='utf8')
