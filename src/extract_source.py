# Author: Andrew Malta 2017

# Unizip the specified zip files and extract all of the files
# of a certain extension (namely the source code) to a neighboring source
# directory.

import os
import sys
import zipfile
from shutil import copyfile

extensions = ["py", "c", "cpp", "java", "js", "r", "pl", "go", "md"]


def unzip_archives(dir_name):
    extension = ".zip"
    os.chdir(dir_name) # change directory from working dir to dir with files

    for item in os.listdir(dir_name): # loop through items in dir
        if item.endswith(".zip"): # check for ".zip" extension
            print "unzipping " + item
            try:
                file_name = os.path.abspath(item) # get full path of files
                zip_ref = zipfile.ZipFile(file_name) # create zipfile object
                zip_ref.extractall(dir_name) # extract file to dir
                zip_ref.close() # close file
                os.remove(file_name) # delete zipped file
            except:
                print "failed unzipping " + item
if __name__ == "__main__":
    argc = len(sys.argv)

    if argc != 2:
        print "Usage: python extract_source.py [relative path in /data to archives]"
        sys.exit(1)

    path = os.path.expanduser(
        "~/Dropbox/classes/Fall 2017/project/data/{}/archives".format(sys.argv[1]))

    unzip_archives(path)

    count = 0
    dest_path = os.path.expanduser("~/Dropbox/classes/Fall 2017/project/data/{}/source/".format(sys.argv[1]))
    if not os.path.isdir(dest_path):
        os.mkdir(dest_path)

    print path
    for root, dirs, files in os.walk(path):
        dirs_in_path = root.split('/')
        if dirs_in_path[-1] != "archives": # make sure we are at least one dir down
            # name of the repo comes right after the archives directory name in the path
            repo = dirs_in_path[dirs_in_path.index("archives") + 1]
        for f in files:
            splt = f.split('.')
            if len(splt) > 1 and splt[1] in extensions:
                name = "{}_{}.{}".format(repo, splt[0], f.split('.')[1])
                copyfile(root + "/" + f, dest_path + name)
                count += 1

    print "Extracted {} files from the archive directory".format(count)

