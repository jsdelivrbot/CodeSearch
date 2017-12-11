from search import *
import pickle as pkl
from collections import Counter

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

if __name__ == "__main__":
    print "reading in json file ... "
    json_dict = read_json_file()

    print "extracting source map ..."
    source_map = build_source_map(json_dict)

    print "extracting functions ..."
    # somehow contained duplicates, so have to remove them
    functions, functions_freq = extract_code_type(json_dict, "function", source_map)

    print "extracting classes ..."
    # somehow contained duplicates, so have to remove them
    classes, classes_freq = extract_code_type(json_dict, "class", source_map)

    print "extracting docstring maps ..."
    function_docstring_map = build_docstring_map(json_dict, functions)
    classes_docstring_map = build_docstring_map(json_dict, classes)

    # print "merging source and docstring maps ..."
    # temp = merge_two_dicts(classes_docstring_map, function_docstring_map)
    # both_map = merge_two_dicts(temp, source_map)

    print "extracting file source code ..."
    files, files_freq = extract_file_tuples(source_map)

    print len(functions), len(classes)
    print len(functions_freq), len(classes_freq), len(files_freq)
    print "pickling results ..."
    with open("indices.pkl", "w") as f:
        pkl.dump((json_dict, source_map, function_docstring_map,
                  classes_docstring_map, functions, functions_freq,
                  classes, classes_freq, files, files_freq), f)
