#!/usr/local/bin/python
import cgi, os
import cgitb; cgitb.enable()
import json
from AviaryFX import AviaryFX
import time

API_KEY = "demoapp"
API_SECRET = "demoappsecret"
UPLOAD_DIR = "uploads/"
#windows filepath
#UPLOAD_DIR = "C:\path\to\dir\\"
aviaryfx = AviaryFX(API_KEY, API_SECRET)

form = cgi.FieldStorage()

try:
    method = form['q'].value
except KeyError:
    pass

#getFilters
def getFilters():
    filters = aviaryfx.getFilters()
    allFilters = []
    for filterInfo in filters:
        filter = {"label" : filterInfo.label, "uid" : filterInfo.uid}
        allFilters.append(filter)
    print "Content-Type: text/plain\n"
    print json.dumps(allFilters)

#upload
def upload():
    fileitem = form['file']
    if fileitem.filename:
        fn = str ( int( time.time() ) ) + "-" + os.path.basename(fileitem.filename)
        open(UPLOAD_DIR + fn, 'wb').write(fileitem.file.read())
        print "Content-Type: text/plain\n"
        uploadResponse = aviaryfx.upload(UPLOAD_DIR + fn)
        os.unlink(UPLOAD_DIR + fn)
    else:
        print 'No file was uploaded'
    print "Content-Type: text/plain\n"
    print json.dumps(uploadResponse)
    
#renderOptions
def renderOptions():
    backgroundColor = "0xFFFFFFFF"
    format = "jpg"
    quality = "100"
    scale = "1"
    filterid = form['filterid'].value
    filepath = form['filepath'].value
    cols = "3"
    rows = "3"
    cellWidth = "128"
    cellHeight = "128"
    renderOptionsResponse = aviaryfx.renderOptions(backgroundColor, format, quality, scale, filepath, filterid, cols, rows, cellWidth, cellHeight)
    print "Content-Type: text/plain\n"
    print json.dumps(renderOptionsResponse)

#render
def render():
    backgroundColor = "0xFFFFFFFF"
    format = "jpg"
    quality = "100"
    scale = "1"
    width = "0"
    height = "0"
    filterid = form['filterid'].value
    filepath = form['filepath'].value
    renderParameters = form['renderParameters'].value
    renderParameters = json.loads(renderParameters)
    renderResponse = aviaryfx.render(backgroundColor, format, quality, scale, filepath, filterid, width, height, renderParameters)
    print "Content-Type: text/plain\n"
    print json.dumps(renderResponse)

#main   
def main():
    if method == "getFilters":
        getFilters()
    if method == "upload":
        upload()
    if method == "renderOptions":
        renderOptions()
    if method == "render":
        render()
    
if __name__ == "__main__":
    main()