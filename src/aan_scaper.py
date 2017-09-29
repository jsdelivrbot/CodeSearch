# Author: Andrew Malta 2017

# helper script to scrape the resource links from AAN, to get
# some high quality github repositories for our code search needs.

import requests

# cycle through the resource links of AAN and record
# the links of the resources in a file.
def grab_aan_resource_links():
    urls = []
    for rid in xrange(0, 10000):
        url = "http://tangra.cs.yale.edu/newaan/index.php/resource/visit/{}".format(rid)
        try:
            r = requests.get(url)
            if len(r.history) > 0: # if we successfully redirected
                print "Adding {}: {}".format(rid, r.url)
                urls.append(r.url)
        except:
            print "failed on {}".format(rid)
            continue


    with open("aan_resource_links.txt", "w") as f:
        for url in urls:
            f.write(url + "\n")

if __name__ == "__main__":
    grab_aan_resource_links()

