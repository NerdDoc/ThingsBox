#!/usr/bin/python

# Thingiverse* exporter
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

downloadFiles = True # If set to false, will link to original files instead of downloading them
redownloadExistingFiles = False # This saves time when re-running the script in long lists (but be careful, it only checks if file already exists -not that it is good-)
singlePage = True
thingBox = True
collectionTitle = "None"
collectionId = ""


# Helper function to show usage
def printUsage():
	print ("Usage: export_thing.py ... [arg1 | arg2 arg3]")
	print ("This script grabbing Thingiverse thing page and converting it to ThingsBox or Thing Tracker autonomous page.\n")
	print ("\targ1 - B or T - grab mode B - complite single page for ThingsBox; T - Thing file for Thing Tracker ")
	print ("\targ2 - Thingiverse thing id")
	print ("\targ3 - Collection Title (if needed)")
	print ("Example: export_thing.py S 12138")
	sys.exit()

if len(sys.argv) == 1:
	printUsage()
for key in sys.argv:
	if key == '/?': printUsage()
	if key == '/h':printUsage()
	if key == '/help':printUsage()
	if key == '-help': printUsage()
	if key == '--help': printUsage()
	if key == 'T':thingBox = False

thingID = sys.argv[2]

if len(sys.argv) == 4:
	collectionTitle = sys.argv[3]
	singlePage = False

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
		return [] # Simulate download OK for existing file
	try:
	    r = requests.get(page, allow_redirects=redir)
	except:
	    time.sleep(10)
	    return httpGet(page, filename, redir)
	if r.status_code != 200:
		print(r.status_code)
		return -1
	if not filename:
		# Remove all non ascii characters
		text = (c for c in r.content if 0 < ord(c) < 127) # changed from r.text to r.content
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
		text = str(BScontent.getText(separator=u' ')) # Won't work with non-ascii characters
	except:
		text = re.sub('<[^<]+?>', '', str(BScontent)) # If there are non-ascii characters, we strip tags manually with a regular expression
	return text.strip() # Remove leading and trailing spaces


print("\nProcessing thing: " + thingID)
print("Loading thing data")

res = httpGet(url + "/thing:" + thingID, redir=False) # Load the page of the thing
if res == -1:
	print("Error while downloading " + thingID + " : " + title)
	exit()
res_xml = BeautifulSoup(res, convertEntities=BeautifulSoup.HTML_ENTITIES)


try:
	header_data = res_xml.findAll("div", { "class":"thing-header-data" })[0]
	title = str(header_data.h1.text.encode('utf-8', 'ignore'))
except:
	title = str(res_xml.findAll("title")[0].text.encode('utf-8', 'ignore'))


title = re.sub("\[[^\]]*\]","", title) # Optional: Remove text within brackets from the title
title = title.strip()

folder = "-".join(re.findall("[a-zA-Z0-9]+", title)) # Create a clean title for our folder

if not singlePage:
	makeDirs(collectionTitle)
	folder = collectionTitle +"/" + folder

makeDirs(folder) # Create the required directories
makeDirs(folder + "/img")
makeDirs(folder + "/zip")
makeDirs(folder + "/src")


description = res_xml.findAll("meta",{ "property":"og:description" })
if description:
	description = "".join(map(str,description))
	description = description.rstrip("\n")
	index = description.find("content=\"")
	lenght = len(description)
	description = description[index+9:lenght]
	if index == -1: description = "None"
	index = description.find("\" />")
	if index != -1:description = description[:index]
	description = description.replace('\n','')
else:
	description = "None"

description_new = res_xml.findAll("div",{ "id":"description" })
if description_new:
	description_new = "".join(str(item) for item in description_new[0].contents)
	description_new = description_new.strip()
	lenght = len(description_new)
	index = description_new.find("mary</h1>")
	description_new = description_new[index+9:lenght]
	if index == -1: description_new = "None"
	index = description_new.find("<h1 class=\"thing")
	if index != -1:description_new = description_new[:index]
	description_new = description_new.replace('"','\\"')
	description_new = description_new.replace('\n','')
else:
	description_new = "None"

postPrinting = res_xml.findAll("div",{ "id":"description" })
if postPrinting:
	postPrinting = "".join(str(item) for item in postPrinting[0].contents)
	postPrinting = postPrinting.strip()
	lenght = len(postPrinting)
	index = postPrinting.find("Post-Printing</h1>")
	postPrinting = postPrinting[index+18:lenght]
	if index == -1: postPrinting = ""
	if index !=-1:
		index = postPrinting.find("<h1 class=\"thing-component-header design how-i-designed-this")
		if index !=-1:
			postPrinting = postPrinting[:index]
	postPrinting = postPrinting.replace('"','\\"')
	postPrinting = postPrinting.replace('\n', '')
else:
	postPrinting = ""


instructions = res_xml.findAll("div",{ "id":"description" })
if instructions:
	instructions = "".join(str(item) for item in instructions[0].contents)
	instructions = instructions.strip()
	lenght = len(instructions)
	index = instructions.find("ctions</h1>")
	instructions = instructions[index+11:lenght]
#	instructions = instructions.find("\">")
#	if index !=-1:instructions = instructions[:index]
	instructions = instructions.replace('"','\\"')
	instructions = instructions.replace('\n', '')
	if index == -1: instructions = ""
else:
	instructions = ""

notes = res_xml.findAll("div",{ "id":"description" })
if notes:
	notes = "".join(str(item) for item in notes[0].contents)
	notes = notes.strip()
	lenght = len(notes)
	index = notes.find("Notes: </strong>")
	notes = notes[index+16:lenght]
	index = notes.find("<h1 class=\"thing-component-header tips post-printing")
	if index !=-1:notes = notes[:index]
	notes = notes.replace('"','\\"')
	notes = notes.replace('\n', '')
	if index == -1: notes = ""
else:
	notes = ""

creatorName = res_xml.findAll("span", { "class":"creator-name" }) # Get creator name
if creatorName:
	creatorName = "".join(str(item) for item in creatorName[0].contents)
	creatorName = creatorName.strip()
	index = creatorName.find("\">")
	lenght = len(creatorName)
	creatorName = creatorName[index+2:lenght]
	if index == -1: creatorName = "None"
	index = creatorName.find("</a>")
	if index !=-1:creatorName = creatorName[:index]
else:
	creatorName = "None"

collectNumber = res_xml.findAll("span", { "class":"interaction-count collection-count" }) # Collection number
if collectNumber:
	collectNumber = "".join(str(item) for item in collectNumber[0].contents)
	collectNumber = collectNumber.strip()
else:
	collectNumber = 0

watchNumber = res_xml.findAll("span", { "class":"interaction-count watch-count" }) # watch number
if watchNumber:
	watchNumber = "".join(str(item) for item in watchNumber[0].contents)
	watchNumber = watchNumber.strip()
else:
	watchNumber = 0

madeNumber = res_xml.findAll("a", { "class":"thing-made" }) #maded
if madeNumber:
	madeNumber = "".join(str(item) for item in madeNumber[0].contents)
	madeNumber = madeNumber.strip()
	index = madeNumber.find("count\">")
	lenght = len(madeNumber)
	madeNumber = madeNumber[index+7:lenght]
	if index == -1: madeNumber = 0
	index = madeNumber.find("</span>")
	if index !=-1:madeNumber = madeNumber[:index]
else:
	madeNumber = 0

remixNumber = res_xml.findAll("a", { "class":"thing-remix" }) #number of remixes
if remixNumber:
	remixNumber = "".join(str(item) for item in remixNumber[0].contents)
	remixNumber = remixNumber.strip()
	index = remixNumber.find("count\">")
	lenght = len(remixNumber)
	remixNumber = remixNumber[index+7:lenght]
	if index == -1: remixNumber = 0
	index = remixNumber.find("</span>")
	if index !=-1:remixNumber = remixNumber[:index]
else:
	remixNumber = 0

remixNumber = str(remixNumber)

viewNumber = res_xml.findAll("span", { "class":"thing-views" }) #number of views
if viewNumber:
	viewNumber = "".join(str(item) for item in viewNumber[0].contents)
	viewNumber = viewNumber.strip()
	index = viewNumber.find("count\">")
	lenght = len(viewNumber)
	viewNumber = viewNumber[index+7:lenght]
	if index == -1: viewNumber = 0
	index = viewNumber.find("</span>")
	if index !=-1:viewNumber = viewNumber[:index]
else:
	viewNumber = 0

downloadNumber = res_xml.findAll("span", { "title":"downloads" }) #number of downloads
if downloadNumber:
	downloadNumber = "".join(str(item) for item in downloadNumber[0].contents)
	downloadNumber = downloadNumber.strip()
	index = downloadNumber.find("count\">")
	lenght = len(downloadNumber)
	downloadNumber = downloadNumber[index+7:lenght]
	if index == -1: downloadNumber = 0
	index = downloadNumber.find("</span>")
	if index !=-1:downloadNumber = downloadNumber[:index]
else:
	downloadNumber = 0

likeNumber = res_xml.findAll("a", { "class":"thing-like loginreq" }) # number of likes
if likeNumber:
	likeNumber = "".join(str(item) for item in likeNumber[0].contents)
	likeNumber = likeNumber.strip()
	index = likeNumber.find("count\">")
	lenght = len(likeNumber)
	likeNumber = likeNumber[index+7:lenght]
	if index == -1: likeNumber = "None"
	index = likeNumber.find("</span>")
	if index !=-1:likeNumber = likeNumber[:index]
else:
	likeNumber = 0

pubTime = res_xml.findAll("span", { "class":"thing-pub-time" }) # Publication time
if pubTime:
	pubTime = "".join(str(item) for item in pubTime[0].contents)
	pubTime = pubTime.strip()
else:
	pubTime = ""

creationDate = res_xml.findAll("div", { "class":"thing-header-data" }) # Get creation date
if creationDate:
	creationDate = "".join(str(item) for item in creationDate[0].contents)
	creationDate = creationDate.strip()
	lenght = len(creationDate)
	index = creationDate.find("time=\"")
	if index !=-1: creationDate = creationDate[index+6:lenght]
	index = creationDate.find("\">")
	if index !=-1:creationDate = creationDate[:index]
	creationDate = creationDate.replace(' GMT','')
else:
	creationDate = "None"

license = res_xml.findAll("div", { "class":"license-text" })
if license:
	license = myGetText(license[0]) # Get the license
	lenght = len(license)
	index = license.find("under the")
	if index !=-1: license = license[index+10:lenght]
else:
	license = "CC-BY-SA"

tags = res_xml.findAll("div", { "class":"thing-info-content thing-detail-tags-container" })
if tags:
	tags = myGetText(tags[0]) # Get the tags
	tags = tags.split()
else:
	tags = ""
if len(tags) < 2: tags = ""




header = res_xml.findAll("div", { "class":"thing-header-data" })
if header:
	header = myGetText(header[0]) # Get the header (title + date published)
else:
	header = "None"
if len(header) < 2: header = "None"


files = {}
for file in res_xml.findAll("div", { "class":"thing-file" }): # Parse the files and download them
	fileUrl = url + str(file.a["href"])
	fileName = str(file.a["data-file-name"])
	filePath = folder + "/src/" + fileName
	if downloadFiles:
		print("Downloading file ( " + fileName + " )")
		httpGet(fileUrl, filePath)
	else:
		print("Skipping download for file: " + fileName + " ( " + fileUrl + " )")

	filePreviewUrl = str(file.img["src"])
	filePreviewPath = filePreviewUrl.split('/')[-1]
	filePreview = folder + "/img/" + filePreviewPath
	print("-> Downloading preview image ( " + filePreviewPath + " )")
	httpGet(filePreviewUrl, filePreview)

	files[filePath] = {}
	files[filePath]["url"] = fileUrl
	files[filePath]["name"] = fileName
	files[filePath]["preview"] = filePreviewPath

ava = res_xml.findAll("div", { "class":"avatar-wrapper" }) #ava
if ava:
	ava = "".join(str(item) for item in ava[0].contents)
	ava = ava.strip()
	index = ava.find("img src=\"")
	lenght = len(ava)
	ava = ava[index+9:lenght]
	if index == -1: ava = 0
	index = ava.find("\" alt")
	if index !=-1:ava = ava[:index]
	avaImgName = ava.split('/')[-1]
	avaImgFile = folder + "/img/" + avaImgName
	print("Downloading  avatar image ( " + avaImgName + " )")
	httpGet(ava, avaImgFile)
else:
	ava = 0


gallery = res_xml.findAll("div", { "class":"thing-page-slider main-slider" })[0]
images = []
for image in gallery.findAll("div", { "class":"thing-page-image featured" }): # Parse the images and download them
	imgUrl = str(image["data-large-url"])
	imgName = imgUrl.split('/')[-1]
	imgFile = folder + "/img/" + imgName
	print("Downloading image ( " + imgName + " )")
	httpGet(imgUrl, imgFile)
	images.append(imgName)


print ("Downloading " + title + ".zip") # Downloading zip of thing
zipUrl =url + "/thing:" + thingID + "/zip"
zipFile = folder + "/zip/" + thingID + ".zip"
httpGet(zipUrl,zipFile)

filenameJson = ""

if not thingBox:
	filenameJson = "tracker.json"
else:
	filenameJson = "thing.json"

# Write in the page for the thing
with open(folder + "/" + filenameJson, 'w') as fd: # Generate the tracker.json or thing.json file for the thing
	if not thingBox:
		fd.write("{\n")
		fd.write("\"id\": \"" + thingID +"\",\n")
		fd.write("\"description\": \"" + header +"\",\n")
		fd.write("\"url\": \"https://www.thingiverse.com/thing:" + thingID +"\",\n")
		fd.write("\"maintainers\": [\n")
		fd.write("\t{\n")
		fd.write("\t\"name\": \"" + creatorName + "\",\n")
		fd.write("\t\"url\": \"https://www.thingiverse.com/thing:" + thingID + "\",\n")
		fd.write("\t\"email\": \"None\"\n")
		fd.write("\t}\n")
		fd.write("\t],\n")
		fd.write("\"things\":[\n")
	fd.write("\t{\n")
	fd.write("\t\"id\": \"" + thingID +"\",\n")
	fd.write("\t\"avatar\": \"thumbnails/" + avaImgFile +"\",\n")
#	fd.write("\t\"collectionTitle\": \"" + collectionTitle + "\",\n")
#	fd.write("\t\"collectionId\": \"" + collectionId + "\",\n")
	fd.write("\t\"title\": \"" + title +"\",\n")
	fd.write("\t\"description\": \""+ description_new +"\",\n")
	fd.write("\t\"url\": \"https://www.thingiverse.com/thing:" + thingID + "\",\n")
	fd.write("\t\"downloadUrl\": \"thumbnails/"+ zipFile + "\",\n")
	fd.write("\t\"like\": \"" + likeNumber +"\",\n")
	fd.write("\t\"collect\": \"" + collectNumber +"\",\n")
	fd.write("\t\"made\": \"" + madeNumber +"\",\n")
	fd.write("\t\"watch\": \"" + watchNumber +"\",\n")
	fd.write("\t\"remix\": \"" + remixNumber +"\",\n")
	fd.write("\t\"views\": \"" + viewNumber +"\",\n")
	fd.write("\t\"downloads\": \"" + downloadNumber +"\",\n")
	fd.write("\"authors\": [\n")
	fd.write("\t{\n")
	fd.write("\t\"name\": \"" + creatorName + "\",\n")
	fd.write("\t\"url\": \"https://www.thingiverse.com/thing:" + thingID + "\",\n")
	fd.write("\t\"email\": \"None\"\n")
	fd.write("\t}\n")
	fd.write("\t],\n")
	fd.write("\"created\": \"" + pubTime + "\",\n")
	fd.write("\"licenses\": [\n")
	fd.write("\t\"" + license +"\"\n")
	fd.write("\t],\n")
	fd.write("\"thumbnailUrls\": [\n")
	lenght = len(images)
	if lenght > 1:
		counter = 0
		for image in images:
			counter = counter+1
			if counter == (lenght):
				fd.write("\t\"thumbnails/" + folder +"/img/" + urllib.quote(image) + "\"\n")
			else:
				fd.write("\t\"thumbnails/" + folder +"/img/" + urllib.quote(image) + "\",\n")
	fd.write("\t],\n")
	fd.write("\"media\": [\n")
	fd.write("\t\"None\"\n")
	fd.write("\t],\n")
	fd.write("\"categories\": [\n")
	fd.write("\t\"None\"\n")
	fd.write("\t],\n")
	fd.write("\"tags\": [\n")
	lenght = len(tags)
	if lenght > 1:
		counter = 0
		for tag in tags:
			if counter == (lenght-1):
				fd.write("\t\"" + tags[counter] + "\"\n")
			else:
				fd.write("\t\"" + tags[counter] + "\",\n")
			counter = counter + 1
	fd.write("\t],\n")
	fd.write("\"billOfMaterials\": [\n")
	lenght = len(files.keys())
	if lenght > 1:
		counter = 0
		for path in files.keys():
			file = files[path]
			fileurl = file["url"]
			if downloadFiles:
				fileurl = file["name"]
			if counter == (lenght-1):
				fd.write("\t{\n")
				fd.write("\t\"partNumber\": \"\",\n")
				fd.write("\t\"description\": \"" + file["name"] + "\",\n")
				fd.write("\t\"url\": \"thumbnails/" + folder + "/src/" + file["name"] +"\",\n")
				fd.write("\t\"type\": \"source\",\n")
				fd.write("\t\"mimetype\": \"\",\n")
				fd.write("\t\"thumbnailUrl\": \"thumbnails/" + folder + "/img/" + urllib.quote(file["preview"]) +"\"\n")
				fd.write("\t}\n")
			else:
				fd.write("\t{\n")
				fd.write("\t\"partNumber\": \"\",\n")
				fd.write("\t\"description\": \"" + file["name"] + "\",\n")
				fd.write("\t\"url\": \"thumbnails/" + folder + "/src/" + file["name"] + "\",\n")
				fd.write("\t\"type\": \"source\",\n")
				fd.write("\t\"mimetype\": \"\",\n")
				fd.write("\t\"thumbnailUrl\": \"thumbnails/" + folder + "/img/" + urllib.quote(file["preview"]) + "\"\n")
				fd.write("\t},\n")
			counter = counter + 1
	fd.write("\t],\n")
	fd.write("\"instructions\": [\n")
	fd.write("\t{\n")
	fd.write("\t\"step\": \"\",\n")
	fd.write("\t\"text\": \"" + instructions +"<br><strong>Notes:</strong> " + notes +"</br><br><strong>PostPrinting:</strong> " + postPrinting + "</br>\",\n")
	fd.write("\t\"images\": \"\"\n")
	fd.write("\t}\n")
	fd.write("\t]\n")

	fd.write("\t}\n")#end of things
	if not thingBox:
		fd.write("\t]\n")
		fd.write("}")

