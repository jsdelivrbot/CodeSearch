import sys
import os
import numpy as np
from collections import Counter
from collections import defaultdict
import json

def read_source(directory_path):
    source_arr = []
    for root, dirs, files in os.walk(directory_path):
        for f in files:
            with open(directory_path + "/" + f, "r") as source:
                s = source.read()
                source_arr.append((f, f.split('_')[0], s))
    return source_arr

def get_file_extensions():
    path = os.path.expanduser("~/Dropbox/classes/Fall 2017/project/data/{}/source/".format("AAN"))
    arr = read_source(path)
    print Counter([a[0].split('.')[-1] for a in arr])

def read_json_file():
    path = os.path.expanduser("~/Dropbox/classes/Fall 2017/project/data/AAN/source_features.json")
    with open(path, "r") as f:
        file_list = json.loads(f.read())
    
    return file_list

def search_for_name(keyword, json_dict, type_filter = None):
    matches = []
    for file_name in json_dict.keys():
        for line in json_dict[file_name]:
            right_type = (type_filter is None or line["type"] == type_filter)
            if line["name"] == keyword and right_type:
                matches.append((file_name, line))
    return matches
    
def search_for_docstring(keyword, json_dict, type_filter = None):
    matches = []
    for file_name in json_dict.keys():
        for line in json_dict[file_name]:
            right_type = (type_filter is None or line["type"] == type_filter)
            if keyword in line["docstring"] and right_type:
                matches.append((file_name, line))
    return matches

def search_for_both(keyword, json_dict, type_filter = None):
    matches = []
    for file_name in json_dict.keys():
        for line in json_dict[file_name]:
            right_type = (type_filter is None or line["type"] == type_filter)
            if keyword in line["docstring"] or keyword in line["name"] and right_type:
                matches.append((file_name, line))
    return matches



def find_matches(json_dict, query, search_type, type_filter=None):
    if search_type == "both":
        matches = search_for_both(query, json_dict, type_filter)
    elif search_type == "docstring":
        matches = search_for_docstring(query, json_dict, type_filter)
    else:
        matches = search_for_name(query, json_dict, type_filter)
    
    if len(matches):
        ends = [infer_end_line(matches[i][0], matches[i][1])
                    for i in xrange(len(matches))]
        return [print_source(matches[i][0], matches[i][1]["line"], ends[i])
                    for i in xrange(len(matches))]
    else:
        return []

def read_source(file_name):
    try:
        with open(file_name, "r") as f:
            source = f.read()
            udata=source.decode("utf-8")
            asciidata=udata.encode("ascii","ignore")
        return asciidata
    except Exception:
        return ""

def print_source(file_name, line_start, line_end):
    source = read_source(file_name)
    return (file_name, line_start, line_end,
            "\n".join(source.split("\n")[line_start - 1 :line_end]))
        

def get_indentation(line_string):
    whitespace = [" ", "\t"]
    indentation = ""
    for char in line_string:
        if char in whitespace:
            indentation += char
        else:
            break
    return indentation

def infer_end_line(file_name, line_dict):
    source = read_source(file_name)
    lines = source.split("\n")
    
    target_indentation = get_indentation(lines[line_dict["line"] - 1])
    i = line_dict["line"]
    while i < len(lines):
        line = lines[i]
        if (get_indentation(line) == target_indentation) and len(line) > 0:
            if i == line_dict["line"]:
                return i
            return i - 1
        i += 1
    return i

if __name__ == "__main__":
    get_file_extensions()
    json_dict = read_json_file()
    print find_matches_by_docstring(json_dict, "softmax", "function")


# Todo
# allow multiple query terms as in a typical search engine and give rankings to ones that contain more of the
# keywords (and higher values to ones that are found next to each other in the document).

# Make a demo query page that you can do the search from. This can be a simple flask application or something.