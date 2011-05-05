# Aviary Effects API Python Library

## Introduction

A library for the Aviary Effects API written in Python.

## Build and Install

1. Download the latest AviaryFX Python Library
2. Extract and run the following commands in the setup folder:

<pre><code>$ python setup.py build 
$ python setup.py install
</code></pre>

## Test

To test run the following command in the example/cgi-bin folder. This will run the methods and print the output to the terminal window.

<pre><code>$ python test.py</code></pre>

## Instantiate an AviaryFX object

The Aviary Effects API is exposed via the AviaryFX class.

To create an instance of the class with your API key and API secret:

<pre><code>from AviaryFX import AviaryFX
API_KEY = "aviarytest"
API_SECRET = "aviarytestsecret"
aviaryfx = AviaryFX(API_KEY, API_SECRET)
</code></pre>

## Get a list of filters

The getFilters() method returns a list of FilterInfo objects that contain the label, uid and description for each filter. These can be used to render images.

To get the list of filters:

<pre><code>filters = aviaryfx.getFilters()
print filters
</pre></code>

## Upload an image to the AviaryFX Service

The upload() method is used to upload image files to the AviaryFX Service to apply effects to them. This method returns a dict with a url to the file on the server. The returned image url should be used for subsequent interactions.

To upload an image:

<pre><code>uploadResponse = aviaryfx.upload(UPLOAD_DIR + "ostrich.jpg")
print uploadResponse
</code></pre>

## Render thumbnails

Use the renderOptions() method to render a thumbnail grid of the image with preset filter options for the selected filter. This returns a dict with a url to the thumbnail grid and render option parameters for each of the requested number of options for the filter.

To render a 3x3 thumbnail grid with 128px x 128px cells:

<pre><code>backgroundColor = "0xFFFFFFFF"
format = "jpg"
quality = "100"
scale = "1"
filepath = "path/to/file/returned/after/upload"
filterid = "28"
cols = "3"
rows = "3"
cellWidth = "128"
cellHeight = "128"
renderOptionsResponse = aviaryfx.renderOptions(backgroundColor, format, quality, scale, filepath, filterid, cols, rows, cellWidth, cellHeight)
print renderOptionsResponse
</code></pre>

## Render full image

Once an option is selected call the render() method along with the filter ID, image url and the parameters for the selected option. This returns a dict with the URL to rendered image.

<pre><code>backgroundColor = "0xFFFFFFFF"
format = "jpg"
quality = "100"
scale = "1"
width = "0"
height = "0"
filepath = "path/to/file/returned/after/upload"
filterid = "22"
renderParameters = [{"id":"Gamma","value":"2.6706531248452734"},{"id":"Smoothing","value":"4"},{"id":"Caption Index","value":"50"}]
renderResponse = aviaryfx.render(backgroundColor, format, quality, scale, filepath, filterid, width, height, renderParameters)
print renderResponse
</code></pre>

## Methods

Check out the official [Aviary Effects API documentation](http://developers.aviary.com/effects-api) for more details about the Aviary Effects API and class methods.

## Feedback and questions

Found a bug or missing a feature? Don't hesitate to create a new issue here on GitHub, post to the [Google Group](http://groups.google.com/group/aviaryapi) or email us.

