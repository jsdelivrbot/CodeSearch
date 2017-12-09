import sys
import os
import numpy as np
from collections import Counter
from collections import defaultdict
import json

PREFIX = "/Users/andrewmalta/Dropbox/classes/Fall 2017/project/data/AAN/"

def read_source(directory_path):
    source_arr = []
    for root, dirs, files in os.walk(directory_path):
        for f in files:
            with open(directory_path + "/" + f, "r") as source:
                s = source.read()
                source_arr.append((f, f.split('_')[0], s))
    return source_arr

def get_file_extensions():
    arr = read_source(PREFIX)
    print Counter([a[0].split('.')[-1] for a in arr])

def read_json_file():
    path = PREFIX + "source_features.json"
    with open(path, "r") as f:
        file_list = json.loads(f.read())
    
    return file_list

def extract_code_type(json_dict, code_type):
    tuples = []
    for f in json_dict:
        for line in json_dict[f]:
            obj = (f, line["type"], line["name"], line["line"])
            if line["type"] == code_type:
                tuples.append(obj)


    filtered_tuples = []

    for t in tuples:
        try:
            end_line = infer_end_line(t[0], t[3])
            new_tup = (t[0], t[1], t[2], t[3], end_line)
            filtered_tuples.append(new_tup)
        except Exception:
            pass


    return filtered_tuples

def extract_file_tuples(source_map):
    tuples = []

    for f in source_map:
        end_line = len(source_map[f].split('\n'))
        tuples.append((f, "file", f, 0, end_line))

    return tuples

def build_source_map(json_dict):
    source_map = {}

    for f in json_dict:
        source_map[f] = read_source(f)

    return source_map

def frequency_helper(query_words, text):
    frequency_counts = [0] * len(query_words)

    for i, word in enumerate(query_words):
        frequency_counts[i] = text.count(word)

    return tuple(frequency_counts)


def extract_frequencies(query, iterable, source_map):
    matches = {}
    
    for tup in iterable:
        # get the selected piece of code to search
        
        selection = "\n".join(source_map[tup[0]].split('\n')[tup[3] : tup[4]])
        frequency = frequency_helper(query, selection)
        # print tup
        # print selection
        # print frequency

        if sum(frequency):
            matches[tup] = frequency

    return matches

def score_matches(query, matches):
    scores = {}
    for m in matches:
        length = m[4] - m[3]
        scores[m] = sum(matches[m]) / float(length)
    return scores


def find_matches(json_dict, query, iterable, source_map):
    query_split = list(set(query.split(' ')))

    matches = extract_frequencies(query_split, iterable, source_map)
    scores = score_matches(query, matches)


    sortable = [(tup, scores[tup]) for tup in scores]
    results = sorted(sortable, key = lambda x: x[1], reverse=True)
    
    if len(results):
        return [(results[i][1], print_source(results[i][0][0], results[i][0][3], results[i][0][4]))
                     for i in xrange(len(results))]
    else:
        return []


def read_source(file_name):
    try:
        with open(file_name, "r") as f:
            source = f.read()
            udata = source.decode("utf-8")
            asciidata = udata.encode("ascii","ignore")
        return asciidata
    except Exception:
        return ""


def print_source(source_name, line_start=None, line_end=None):
    file_name = source_name
    source = read_source(file_name)
    lines = source.split("\n")


    if line_start == None or line_end == None:
        return (source_name, 0, len(lines), source)
    else:
        return (source_name, line_start, line_end,
            "\n".join(lines[0 if line_start == 0 else line_start - 1: line_end])) 


def get_indentation(line_string):
    whitespace = [" ", "\t"]
    indentation = ""
    for char in line_string:
        if char in whitespace:
            indentation += char
        else:
            break
    return indentation


def infer_end_line(file_name, line_num):
    source = read_source(file_name)
    lines = source.split("\n")
    
    target_indentation = get_indentation(lines[line_num - 1])
    i = line_num
    while i < len(lines):
        line = lines[i]
        if (get_indentation(line) == target_indentation) and len(line) > 0:
            if i == line_num:
                return i
            return i - 1
        i += 1
    return i
