# Author: Andrew Malta 2017


# description

from find_source_files import *
import os
import numpy as np

if __name__ == "__main__":
    data_path = os.path.expanduser("~/Dropbox/classes/Fall 2017/project/data")
    aan_links_path = data_path + "/aan_resource_links.txt"
    download_path = data_path + "/AAN"

    with open(aan_links_path, "r") as f:
        links = f.read().split('\n')

    github_prefix = "https://github.com"
    n = len(github_prefix)

    # turn the github urls into (owner, repository_name) tuples that we can pass
    # to our function download_zip_archives from src/find_source_files.py
    github_tups = [tuple(l[n + 1:].split("/")[0:2]) for l in links if l[0:n] == github_prefix] 


    download_zip_archives(github_tups, download_path)

