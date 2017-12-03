# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, Markup
from search import read_json_file, find_matches
import re



app = Flask(__name__)
json_dict = read_json_file()


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


@app.route('/', methods=['GET'])
def main_handler():
    return render_template("main.html")

@app.route('/search')
def search_handler():
    query = request.args.get('query')
    filter_option = request.args.get('filter')
    search_type = request.args.get('search_type')

    if filter_option == "all":
        filter_option = None

    results = find_matches(json_dict, query, search_type, filter_option)


    n = len(results)
    if n == 0:
        return render_template("results.html", code="No Matches Found.")

    code = []
    for i in xrange(n):
        code.append(Markup(highlight_matches(query.split(' '), results[i][3])))

    matches = [(results[i][0], results[i][1], results[i][2], code[i]) for i in xrange(n)]


    return render_template("results.html", matches=matches)



