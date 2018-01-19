#!/usr/bin/python

# Thingiverse* collection exporter forThingBox and Thing Tracker
# by NerdDoc
# CC-BY-SA license (http://creativecommons.org/licenses/by-sa/3.0/)
# *Unofficial program, not associated with Thingiverse
# Use at your own risk!

# Modules
import requests
from BeautifulSoup import BeautifulSoup
import os
import re
import urllib
import time
import sys
import subprocess

downloadFiles = True  # If set to false, will link to original files instead of downloading them
redownloadExistingFiles = False  # This saves time when re-running the script in long lists (but be careful, it only checks if file already exists -not that it is good-)
not_last_page = True
thingBox = True

# Helper function to show usage
def printUsage():
    print ("Usage: export_collection.py ... [arg1  arg2  arg3]")
    print ("This script grabbing Thingiverse collection and converting it toThingBox or Thing Tracker thing pages.\n")
    print ("\targ1 - B or T - grab mode B - complite single page for ThingsBox; T - Thing file for Thing Tracker ")
    print ("\targ2 - Thingiverse user nick")
    print ("\targ3 - Thingiverse collection title\n")
    print ("Example: export_collection.py Username CollectionTitle")
    sys.exit()


if len(sys.argv) == 1:
    printUsage()
if len(sys.argv) == 2:
    printUsage()
for key in sys.argv:
    if key == '/?': printUsage()
    if key == '/h': printUsage()
    if key == '/help': printUsage()
    if key == '-help': printUsage()
    if key == '--help': printUsage()
    if key == 'T': thingBox = False

userNick = sys.argv[2]
collectionTitle = sys.argv[3]
title = collectionTitle.lower()
title = "-".join(re.findall("[a-zA-Z0-9]+", title))

url = "https://www.thingiverse.com"


# Helper function to create directories
def makeDirs(path):
    try:
        os.makedirs(path)
    except:
        return -1
    return 0


# Helper function to perform the required HTTP requests
def httpGet(page, filename=False, redir=True):
    if filename and not redownloadExistingFiles and os.path.exists(filename):
        return []  # Simulate download OK for existing file
    try:
        r = requests.get(page, allow_redirects=redir)
    except:
        time.sleep(10)
        return httpGet(page, filename, redir)
    if r.status_code == 404:
        global not_last_page
        not_last_page = False
        return - 1
    if r.status_code != 200:
        print(r.status_code)
        return -1
    if not filename:
        # Remove all non ascii characters
        text = (c for c in r.content if 0 < ord(c) < 127)  # changed from r.text to r.content
        text = ''.join(text)
        return text.encode('ascii', 'ignore')
    else:
        with open(filename, 'wb') as fd:
            for chunk in r.iter_content(512):
                fd.write(chunk)
            fd.close()
        return r.history


# Helper function to remove all html tags and format to a BeautifulSoup object
# This is a patch, since the getText function gives problems with non-ascii characters
def myGetText(BScontent):
    try:
        text = str(BScontent.getText(separator=u' '))  # Won't work with non-ascii characters
    except:
        text = re.sub('<[^<]+?>', '', str(
            BScontent))  # If there are non-ascii characters, we strip tags manually with a regular expression
    return text.strip()  # Remove leading and trailing spaces

print("\nProcessing collection from user: " + collectionTitle + " from " + userNick)
print("Loading collection data")
pageNumber = 1;
thingCounter = 0
thingsTotal = 0

while (not_last_page):#Lets try to get next page of collection until we are not get page 404
    res = httpGet(url + "/" + userNick + "/collections/" + title + "/page:" + str(pageNumber), redir=False)  # Load the page of the thing
    if not_last_page == False:
        print ("\nDone with " + collectionTitle + " collection")
        print ("\n Total things: " + str(thingsTotal))
        print ("\nHave a GOOD DAY and GOOD LUCK!!!")
        exit()
    if res == -1:
        print("Error while downloading " + userNick + "/collections/" + collectionTitle)
        exit()
    print ("Page: " + str(pageNumber))
    res_xml = BeautifulSoup(res, convertEntities=BeautifulSoup.HTML_ENTITIES)

    try:
        header_data = res_xml.findAll("div", {"class": "thing-header-data"})[0]
        title = str(header_data.h1.text.encode('utf-8', 'ignore'))
    except:
        title = str(res_xml.findAll("title")[0].text.encode('utf-8', 'ignore'))

    collectionId = res_xml.find("div", {"class": "thing-interact thingcollection-edit"})['data-link']
    if not collectionId:
        collectionId = 'None'


    for thing in res_xml.findAll("div", {"class": "thing thing-interaction-parent item-card"}):
        thingId = thing.get('data-thing-id')
        thingCounter = thingCounter + 1
    with open(os.getcwd() + "/" + collectionTitle + ".json", 'w') as fd:  # Generate the collection.json file
        fd.write("{\n")
        fd.write("\"collectionTitle\": \"" + collectionTitle + "\",\n")
        fd.write("\"ThingsId\": [\n")
        for thing in res_xml.findAll("div", {"class": "thing thing-interaction-parent item-card"}):
            thingId = thing.get('data-thing-id')
            if not thingBox:
                return_code = subprocess.call([os.getcwd() + "/export_thing.py", "T", thingId, collectionTitle])
            else:
                return_code = subprocess.call([os.getcwd() + "/export_thing.py", "B", thingId, collectionTitle])
            print (return_code)
            if return_code == 0:
                thingsTotal = thingsTotal + 1
                if thingCounter != 1:
                    fd.write("\t\"" + thingId + "\",\n")
                    thingCounter = thingCounter - 1
                else:
                    fd.write("\t\"" + thingId + "\"\n")
                    print ("Thing: " + thingId + " Grabbed - OK!")
            else:
                print ("Thing: " + thingId + " Grab ERROR!!!")
        fd.write("\t]\n")
        fd.write("}\n")
    pageNumber = pageNumber + 1


