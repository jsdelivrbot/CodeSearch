# Author: Andrew Malta 2017
# Older functions used in previous iterations of the github scrape

import requests
from lxml import html

def get_repo_tree_scrape(owner, repo, path, recursive=True):
    url = "https://github.com/{}/{}".format(owner, repo)

    wait_for_rate_limiter("core", 1000)
    print "requesting {}".format(url)
    r = requests.get(url)

    tree = html.fromstring(r.text)

    result = tree.find_class("files js-navigation-container")
    tbody = [child for child in result[0].iterchildren()][0]

    for child in tbody.iterchildren():
        children = child.getchildren()

        files = []

        if len(child.getchildren()) == 4:
            icon_value = children[0].getchildren()[0].values()[1]
            file_type = icon_value[len("octicon octicon-file-"):]
            name = children[1].getchildren()[0].text_content()

            if file_type == "directory" and recursive:
                files += get_repo_tree(owner, repo, path + name + "/")
            else:
                print path + name
                files.append(path + name)
    return files
