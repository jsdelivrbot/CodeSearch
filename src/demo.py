# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Markup
from search import *
import re
import pickle as pkl
import cgi

app = Flask(__name__)

with open("indices.pkl", "r") as f:
    json_dict, source_map, functions, classes, files = pkl.load(f)

def highlight_matches(words, s):
    output = ''
    pairs = []
    for word in words:
        for m in re.finditer(word, s):
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
    source = print_source(name)[-1]
    return render_template("code.html", source=source)


@app.route('/search')
def search_handler():
    query = request.args.get('query')
    filter_option = request.args.get('filter')
    # search_type = request.args.get('search_type')

    if filter_option == "function":
        iterable = functions
    elif filter_option == "class":
        iterable = classes
    else:
        iterable = files

    results = find_matches(json_dict, query, iterable, source_map)[0:10]

    n = len(results)
    if n == 0:
        return render_template("results.html", code="No Matches Found.")

    code = []
    scores = []
    for i in xrange(n):
        tup = results[i][1]
        scores.append(results[i][0])
        source_code = cgi.escape(tup[3])
        code.append(Markup(highlight_matches(query.split(' '), source_code)))

    matches = [(results[i][1][0], results[i][1][1], results[i][1][2], code[i], scores[i])
                    for i in xrange(n)]


    return render_template("results.html", matches=matches)



