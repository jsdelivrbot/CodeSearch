import sys
import os
import numpy as np
from collections import Counter
from collections import defaultdict
import json
import math
import re

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

def extract_code_type(json_dict, code_type, source_map):
    tuples = []
    for f in json_dict:
        for line in json_dict[f]:
            obj = (f, line["type"], line["name"], line["line"])
            if line["type"] == code_type:
                tuples.append(obj)


    filtered_tuples = []
    frequencies_map = {}
    global_frequencies = defaultdict(int)

    for t in tuples:
        try:
            end_line = infer_end_line(t[0], t[3])
            selection = "\n".join(source_map[t[0]][0].split('\n')[t[3] : end_line])
            frequencies = gen_source_frequencies(selection)
            
            for word in frequencies:
                global_frequencies[word] += 1

            new_tup = (t[0], t[1], t[2], t[3], end_line)
            frequencies_map[new_tup] = frequencies
            filtered_tuples.append(new_tup)
        except Exception:
            pass

    return filtered_tuples, (frequencies_map, global_frequencies)

def extract_file_tuples(source_map):
    tuples = []
    frequencies_map = {}
    global_frequencies = defaultdict(int)

    for f in source_map:
        end_line = len(source_map[f][0].split('\n'))
        

        new_tup = (f, "file", f, 0, end_line)
        frequencies_map[new_tup] = source_map[f][1]
        for word in source_map[f][1]:
            global_frequencies[word] += 1

        tuples.append(new_tup)

    return tuples, (frequencies_map, global_frequencies)

def gen_source_frequencies(text):
    results = []
    tokens = text.split()

    replace_chars = ",()\"\'_-[]{}:;./\\=*#%^"
    for t in tokens:
        new_str = ""
        for c in t:
            if c in replace_chars:
                new_str += ' '
            else:
                new_str += c

        new_tokens = new_str.split(' ')
        results += new_tokens

    final_results = []
    for t in results:
        un_camel_case = [val.lower() for val in re.sub('([a-z])([A-Z])', r'\1 \2', t).split()]
        final_results += un_camel_case
        final_results += t

    return Counter(final_results)

def build_source_map(json_dict):
    source_map = {}

    for f in json_dict:
        source = read_source(f)
        frequencies = gen_source_frequencies(source)
        source_map[f] = (source, frequencies)

    return source_map

def build_docstring_map(json_dict, tuples):
    docstring_map = {}

    for t in tuples:
        file_name = t[0]
        for line in json_dict[file_name]:
            name = t[2]
            if line["name"] == name:
                docstring = line["docstring"]
                frequencies = gen_source_frequencies(docstring)
                docstring_map[t] = (docstring, frequencies)
                break

    return docstring_map

def frequency_helper(query_words, text):
    frequency_counts = [0] * len(query_words)

    for i, word in enumerate(query_words):
        frequency_counts[i] = text.count(word)

    return tuple(frequency_counts)


def filter_frequencies(query, iterable, iterable_frequencies, content_map, using_source_map):
    matches = set()
    for f in iterable:
        counts = [0] * len(query)
        # if using_source_map:
        #     frequencies = content_map[f[0]][1]
        # else:
        #     frequencies = content_map[f][1]
        frequencies = iterable_frequencies[f]

        for i, word in enumerate(query):
            if word in frequencies:
                counts[i] = frequencies[word]

        if sum(counts):
            matches.add(f)

    return matches

def score_matches(query, n, matches, iterable_frequencies, global_frequencies, content_map, using_source_map):
    scores = {}

    for m in matches:
        name_score = 0.0
        frequencies = iterable_frequencies[m]

        tf_normalizer = .75 * len(frequencies) + .25 * (m[4] - m[3])
        if m[4] - m[3] == 0:
            continue

        name_freq = gen_source_frequencies(m[2])
        tfidf_score = 0.0
        for word in query:
            if word in name_freq:
                name_score += 1.0

            if word in frequencies:
                # avoid division by zero in either case here
                tf_score = frequencies[word] / float(tf_normalizer)
                idf_score = math.log(float(n) / (1 + global_frequencies[word]))
                tfidf_score += tf_score * idf_score

        scores[m] = name_score + tfidf_score

    return scores


def find_matches(json_dict, query, iterable, frequencies_ds, content_map, using_source_map):
    query_split = list(set(query.split(' ')))
    iterable_frequencies, global_frequencies = frequencies_ds

    matches = filter_frequencies(query_split, iterable, iterable_frequencies, content_map, using_source_map)
    scores = score_matches(query, len(iterable), matches, iterable_frequencies, global_frequencies, content_map, using_source_map)

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
