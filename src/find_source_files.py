# Author: Andrew Malta 2017

# primary file for finding repositories of a particular language containing certain keywords
# and downloading the archives of the respositories.

import requests
from lxml import html
import sys
import time
import os

def find_lang_repos(language, search_term):
    tups = []
    temp = "https://api.github.com/search/repositories?q={}+in:file+language:{}&sort=stars&order=desc"
    url = temp.format(search_term, language)
    auth = (os.environ.get("GITHUB_USER"), os.environ.get("GITHUB_PASS"))

    r = requests.get(url, auth=auth)
    json = r.json()
    for item in json["items"]:
        user = item["owner"]["login"]
        repo = item["name"]
        tups.append((user, repo))
    return tups

def wait_until_ms(ms):
    now = time.time()
    to_sleep = (ms - now) + 100 # number of ms to sleep
                                # add 100ms in case we 
                                # don't end up waiting long enough
    time.sleep(float(to_sleep) / 1000)
    assert time.time() > ms 

# busy wait during time that github imposes rate limiting. 
def wait_for_rate_limiter(api_type, abuse_detector_wait_time=.25):
    url = "https://api.github.com/rate_limit"
    r = requests.get(url)
    json = r.json()

    if json["resources"][api_type]["remaining"] > 0:
        time.sleep(abuse_detector_wait_time) # avoid bashing the endpoint too quickly
                                             # to get around the abuse detector
        return
    else:
        wait_until_ms(json["resources"][api_type]["reset"])
        return

def get_archive_link(owner, repo):
    url = "https://api.github.com/repos/{}/{}/zipball/master".format(owner, repo)
    r = requests.get(url)
    print r.text

def download_file(url, name, language):
    language_path = os.path.expanduser("~/Dropbox/classes/Fall 2017/project/data/{}".format(language))
    archives_path = language_path + "/" + "archives" # path to store the archives in the langauge directory
    file_path = archives_path + "/" + name

    # Make the directories if needed
    if not os.path.isdir(language_path):
        os.mkdir(language_path)
    if not os.path.isdir(archives_path):
        os.mkdir(archives_path)

    # grab the archive file from the url and write it out
    r = requests.get(url, stream=True)
    with open(file_path, 'wb') as f:
        for chunk  in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def download_zip_archives(language, repo_tups):
    archive = lambda x, y: "https://api.github.com/repos/{}/{}/zipball/master".format(x, y)
    archive_links = [archive(tup[0], tup[1]) for tup in repo_tups]

    for i, link in enumerate(archive_links):
        name = repo_tups[i][1] + ".zip"
        download_file(link, name, language)
        print "downloaded {}".format(name)
        wait_for_rate_limiter("core", 1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: python find_source_files.py [Language] [Search Terms]^*"

    language = sys.argv[1]
    search_terms = sys.argv[2:]
    repo_tups = find_lang_repos(language, search_terms)
    download_zip_archives(language, repo_tups)

