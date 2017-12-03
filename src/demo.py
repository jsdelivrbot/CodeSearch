from flask import Flask, render_template, request
from search import read_json_file, find_matches_by_docstring
app = Flask(__name__)


json_dict = read_json_file()

@app.route('/', methods=['POST', 'GET'])
def main_handler():
    if request.method == "GET":
        return render_template("main.html")
    elif request.method == "POST":
        query = request.form['query']
        return query

@app.route('/search')
def search_handler():
    query = request.args.get('query')
    results = find_matches_by_docstring(json_dict, query, "function")
    return render_template("results.html", code=results)