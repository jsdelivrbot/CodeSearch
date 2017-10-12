import jedi
import os
import sys
import json
from collections import defaultdict


def get_docstrings_tups(source):
    tups = []
    try:
        defs = jedi.names(source)
    except Exception:
        return []
    for definition in defs
        if definition.type in ["function", "class", "statement"]:
            tups.append((definition.type, definition.name, definition.docstring()))
    return tups


if __name__ == "__main__":
    path = os.path.expanduser("~/Dropbox/classes/Fall 2017/project/data/AAN/source/")
    tokendict = defaultdict(list)

    for root, dirs, files in os.walk(path):
        for item in files:
            if item.endswith(".py"):
                with open(path + item, "r") as f:
                    source = f.read()
                    for t in get_docstrings_tups(source):
                        tokendict[path + item].append(t)

                print "Finished reading tokens in {}".format(path + item)

    output_path = path = os.path.expanduser("~/Dropbox/classes/Fall 2017/project/data/AAN/source_features.json")
    with open(output_path, "w") as f:
        f.write(json.dumps(tokendict))

