# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Markup
from search import *
import re
import pickle as pkl
import cgi

app = Flask(__name__)

with open("indices.pkl", "r") as f:
    (json_dict, source_map, func_doc_map, class_doc_map,
     functions, functions_freq, classes, classes_freq,
     files, files_freq) = pkl.load(f)

def highlight_matches(words, s):
    output = ''
    pairs = []
    for word in words:
        for m in re.finditer(word, s, flags=re.IGNORECASE):
            pairs.append((m.start(), m.end()))

    pairs = sorted(pairs, key = lambda x: x[0])

    output_index = 0
    for p in pairs:
        if output_index < p[0]:
            output += s[output_index: p[0]]

        output += "<mark>" + s[p[0]: p[1]] +"</mark>"
        output_index = p[1]

    output += s[output_index:]
    return output

@app.route('/')
def main_handler():
    return render_template("main.html")

@app.route('/code')
def code_handler():
    name = request.args.get('name')
    name = name.replace('+', ' ')
    source = print_source(name)[-1]
    return render_template("code.html", source=source)


@app.route('/search')
def search_handler():
    query = request.args.get('query')
    filter_option = request.args.get('filter')
    search_type = request.args.get('search_type')

    if filter_option == "file" and search_type == "docstring":
        return render_template("error.html", error="Cant search file by docstring.")

    using_source_map = False
    if filter_option == "function":
        iterable = functions
        iterable_freq = functions_freq
    elif filter_option == "class":
        iterable = classes
        iterable_freq = classes_freq
    elif filter_option == "file":
        iterable = files
        iterable_freq = files_freq
    else:
        return render_template("error.html", error="Illegal filter type")

    if search_type == "code":
        content_map = source_map
        using_source_map = True
    elif search_type == "docstring":
        content_map = func_doc_map if filter_option == "function" else class_doc_map
    else:
        return render_template("error.html", error="Illegal search type")


    results = find_matches(json_dict, query, iterable, iterable_freq, content_map, using_source_map)
    results = results[0:10]

    n = len(results)
    if n == 0:
        return render_template("error.html", error="No Matches Found")

    code_prefix = "/Users/andrewmalta/Dropbox/classes/Fall 2017/project/data/AAN/"
    code = []
    scores = []

    for i in xrange(n):
        tup = results[i][1]
        scores.append(results[i][0])
        source_code = cgi.escape(tup[3])
        code.append(Markup(highlight_matches(query.split(' '), source_code)))


    normalize_path = lambda path: path.replace(' ', '+')

    matches = [(normalize_path(results[i][1][0]), results[i][1][1],
                results[i][1][2], code[i], scores[i]) for i in xrange(n)]


    return render_template("results.html", matches=matches)



