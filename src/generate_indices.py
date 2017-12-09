from search import *
import pickle as pkl

json_dict = read_json_file()
source_map = build_source_map(json_dict)

functions = extract_code_type(json_dict, "function")
classes = extract_code_type(json_dict, "class")
files = extract_file_tuples(source_map)

with open("indices.pkl", "w") as f:
    pkl.dump((json_dict, source_map, functions, classes, files), f)