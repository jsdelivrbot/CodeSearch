# Author: Andrew Malta 2017

# Unizip the specified zip files and extract all of the files
# of a certain extension (namely the source code) to a neighboring source
# directory.

import os
import sys
import zipfile
from shutil import copyfile

def unzip_archives(dir_name):
    extension = ".zip"
    os.chdir(dir_name) # change directory from working dir to dir with files

    for item in os.listdir(dir_name): # loop through items in dir
        if item.endswith(extension): # check for ".zip" extension
            print "unzipping " + item
            file_name = os.path.abspath(item) # get full path of files
            zip_ref = zipfile.ZipFile(file_name) # create zipfile object
            zip_ref.extractall(dir_name) # extract file to dir
            zip_ref.close() # close file
            os.remove(file_name) # delete zipped file

if __name__ == "__main__":
    argc = len(sys.argv)

    if argc != 3:
        print "Usage: python extract_source.py [language] [extension]"
        sys.exit(1)

    language = sys.argv[1]
    extension = sys.argv[2]

    path = os.path.expanduser("~/Dropbox/classes/Fall 2017/project/data/{}/archives".format(language))

    unzip_archives(path)

    count = 0
    dest_path = os.path.expanduser("~/Dropbox/classes/Fall 2017/project/data/{}/source/".format(language))
    if not os.path.isdir(dest_path):
        os.mkdir(dest_path)

    for root, dirs, files in os.walk(path):
        dirs_in_path = root.split('/')
        if dirs_in_path[-1] != "archives": # make sure we are at least one dir down
            # name of the repo comes right after the archives directory name in the root
            repo = dirs_in_path[dirs_in_path.index("archives") + 1]

        for f in files:
            if f.endswith(extension):
                name = "{}_{}.{}".format(repo, count, extension)
                copyfile(root + "/" + f, dest_path + name)
                count += 1

    print "Extracted {} {} files from the archive directory".format(language, count)

