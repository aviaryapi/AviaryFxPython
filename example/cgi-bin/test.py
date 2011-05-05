#!/usr/local/bin/python
from AviaryFX import AviaryFX

API_KEY = "demoapp"
API_SECRET = "demoappsecret"
UPLOAD_DIR = "uploads/"
#windows filepath
#UPLOAD_DIR = "C:\path\to\uploads\folder\\"
aviaryfx = AviaryFX(API_KEY, API_SECRET)

def getFilters():
    filters = aviaryfx.getFilters()
    print filters

def upload():
    uploadResponse = aviaryfx.upload(UPLOAD_DIR + "ostrich.jpg")
    print uploadResponse
    return uploadResponse['url']
    
def renderOptions(uploadedFileUrl):
    backgroundColor = "0xFFFFFFFF"
    format = "jpg"
    quality = "100"
    scale = "1"
    filterid = "22"
    filepath = uploadedFileUrl
    cols = "3"
    rows = "3"
    cellWidth = "128"
    cellHeight = "128"
    renderOptionsResponse = aviaryfx.renderOptions(backgroundColor, format, quality, scale, filepath, filterid, cols, rows, cellWidth, cellHeight)
    print renderOptionsResponse

def render(uploadedFileUrl):
    backgroundColor = "0xFFFFFFFF"
    format = "jpg"
    quality = "100"
    scale = "1"
    width = "0"
    height = "0"
    filterid = "22"
    filepath = uploadedFileUrl
    renderParameters = [{"id":"Gamma","value":"2.6706531248452734"},{"id":"Smoothing","value":"4"},{"id":"Caption Index","value":"50"}]
    renderResponse = aviaryfx.render(backgroundColor, format, quality, scale, filepath, filterid, width, height, renderParameters)
    print renderResponse
        
if __name__ == "__main__":
    print "\n Testing getFilters \n"
    getFilters()
    print "\n Testing upload \n"
    uploadedFileUrl = upload()
    print "\n Testing renderOptions \n"
    renderOptions(uploadedFileUrl)
    print "\n Testing render \n"
    render(uploadedFileUrl)
    print "\n"
