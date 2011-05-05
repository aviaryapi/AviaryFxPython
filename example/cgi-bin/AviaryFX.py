'''
AviaryFX Python SDK

@version: 1.0
@author: Bruce Drummond
@contact: http://www.aviary.com
'''

import time
import hashlib
import urllib
import urllib2
from xml.dom import minidom
import os
from urllib2 import URLError

class AviaryFX(object):
    '''
    Class holding the methods to use the AviaryFX API - upload, renderOptions and render
    '''
    
    VERSION = "0.2"
    PLATFORM = "web"
    HARDWARE_VERSION = "1.0"
    SOFTWARE_VERSION = "Python"
    APP_VERSION = "1.0"

    SERVER = "http://cartonapi.aviary.com/services"
    GET_TIME_URL = "/util/getTime"
    GET_FILTERS_URL = "/filter/getFilters"
    UPLOAD_URL = "/ostrich/upload"
    RENDER_URL = "/ostrich/render"
    
    def __init__(self, api_key, api_secret):
        '''
        Instantiate a new AviaryFX object.
        
        @param api_key: API key
        @type api_key: str
        @param api_secret: API secret
        @type api_secret: str
        '''
        self.api_key = api_key
        self.api_secret = api_secret
        self.defaultParams = { "api_key" : self.api_key, "platform" : self.PLATFORM, "hardware_version" : self.HARDWARE_VERSION, 
                              "software_version" : self.SOFTWARE_VERSION, "app_version" : self.APP_VERSION, "version" : self.VERSION }
        
    def getFilters(self):
        '''
        Gets a list of available filters.
        
        @return: List of FilterInfo objects each of which contains label, uid, description and parameter list for each filter.
        @rtype: list 
        '''
        params = self.defaultParams.copy()
        params["ts"] = self.getTime() 
        params["api_sig"] = self.getApiSignature(params)
        url = self.SERVER + self.GET_FILTERS_URL
        result = self.request(url, params)
        xml = minidom.parse(result)
        self.filters = []
        for node in xml.getElementsByTagName("filter"):
            label = node.getAttribute("label")
            uid = node.getAttribute("uid")
            description = node.getElementsByTagName("description")[0].firstChild.data
            parameters = []
            for parametersNode in node.getElementsByTagName("filtermetadata"):
                parameter = []
                for parameterNode in parametersNode.getElementsByTagName("parameter"):
                    nodeAttributes = []
                    for key in parameterNode.attributes.keys():
                        nodeAttributes.append({ key : parameterNode.getAttribute(key) })
                    parameter.append({ "parameter" : nodeAttributes})
                parameters.append(parameter)
            filter = FilterInfo(label, uid, description, parameters)
            self.filters.append(filter)
        return self.filters
    
    def upload(self, pathToFile):
        '''
        Uploads an image to the Aviary server.
        
        @param pathToFile: Path to the file to be uploaded
        @type pathToFile: str
        @return: Dictionary with url to the uploaded file
        @rtype: dict    
        '''
        params = self.defaultParams.copy()
        params["ts"] = self.getTime() 
        params["api_sig"] = self.getApiSignature(params)
        url = self.SERVER + self.UPLOAD_URL
        params = { 'file1' : file(pathToFile, 'rb'), "api_key" : self.api_key, "platform" : self.PLATFORM, "hardware_version" : self.HARDWARE_VERSION, 
                  "software_version" : self.SOFTWARE_VERSION, "app_version" : self.APP_VERSION, "version" : self.VERSION, "ts" : params["ts"], 
                  "api_sig" : params["api_sig"] }
        opener = urllib2.build_opener(MultipartPostHandler)
        response = opener.open(url, params)
        xml = minidom.parse(response)
        for fileNode in xml.getElementsByTagName("file"):
            for key in fileNode.attributes.keys():
                url = fileNode.getAttribute("url")
        uploadedImage = { "url" : url }
        return uploadedImage
    
    def renderOptions(self, backgroundColor, format, quality, scale, filepath, filterID, cols, rows, cellWidth, cellHeight):
        '''
        Renders a filter options thumbnail grid and returns render parameters for each option.
        
        @param backgroundColor: Background color for transparent uploads. Format: Hex values for Red Green Blue Alpha. Example: 0xFFFFFFFF
        @type backgroundColor: str
        @param format: Rendered file format - JPG/PNG.
        @type format: str
        @param quality: Rendered file quality for JPG files. Value from 1-100
        @type quality: str
        @param scale: Scale of the image. Value 0.0-1.0.
        @type scale: str
        @param filepath: The url retrieved using the upload method.
        @type filepath: str
        @param filterID: ID of the filter
        @type filterID: str
        @param cols: The number of columns to render in thumbnail grid.
        @type cols: str
        @param rows: The number of rows to render in thumbnail grid.
        @type rows: str
        @param cellWidth: The width of each cell in thumbnail grid.
        @type cellWidth: str
        @param cellHeight: The height of each cell in thumbnail grid
        @type cellHeight: str
        @return: Dictionary with url to thumbnail grid and reder option parameters
        @rtype: dict   
        '''
        params = self.defaultParams.copy()
        params["ts"] = self.getTime()
        params["backgroundcolor"] = backgroundColor
        params["format"] = format
        params["quality"] = quality
        params["scale"] = scale
        params["filepath"] = filepath
        params["filterid"] = filterID
        params["cols"] = cols
        params["rows"] = rows
        params["cellwidth"] = cellWidth
        params["cellheight"] = cellHeight
        params["calltype"] = "filteruse"
        params["api_sig"] = self.getApiSignature(params)
        result = self.request(self.SERVER + self.RENDER_URL, params)
        xml = minidom.parse(result)
        parameters = []
        for node in xml.getElementsByTagName("ostrichrenderresponse"):
            renderedImage = xml.getElementsByTagName("url")[0].firstChild.data
            for parametersNode in xml.getElementsByTagName("parameters"):
                parameter = []
                for parameterNode in parametersNode.getElementsByTagName("parameter"):
                    id = parameterNode.getAttribute("id")
                    value = parameterNode.getAttribute("value")
                    parameterAtts = { "id" : id, "value" : value }
                    parameter.append(parameterAtts)
                parameters.append(parameter)
        response = { "renderOptionsGrid" : renderedImage, "renderOptionParams" : parameters }
        return response
    
    def render(self, backgroundColor, format, quality, scale, filepath, filterID, width, height, renderParameters):
        '''
        Renders image based on render parameters.
        
        @param backgroundColor: Background color for transparent uploads. Format: Hex values for Red Green Blue Alpha. Example: 0xFFFFFFFF
        @type backgroundColor: str
        @param format: Rendered file format - JPG/PNG.
        @type format: str
        @param quality: Rendered file quality for JPG files. Value from 1-100
        @type quality: str
        @param scale: Scale of the image. Value 0.0-1.0.
        @type scale: str
        @param filepath: The url retrieved using AviaryFX->upload.
        @type filepath: str
        @param filterID: ID of the filter.
        @type filterID: str
        @param width: The width of the rendered image. 0 returns original width.
        @type width: str
        @param height: The height of the rendered image. 0 returns original height.
        @type height: str
        @param renderParameters: (Optional) Filter render parameters retrieved from AviaryFX.renderOptions()
        @type renderParameters: list
        @return: Dictionary with URL to rendered image
        @rtype: dict
        '''
        parameters = []
        parameters.append( "<parameters>" )
        for parameter in renderParameters:
            parameters.append( '<parameter id="%(id)s" value="%(value)s" />' %parameter )
        parameters.append( "</parameters>" )
        parameters = "".join(parameters)
        
        params = self.defaultParams.copy()
        params["ts"] = self.getTime()
        params["backgroundcolor"] = backgroundColor
        params["format"] = format
        params["quality"] = quality
        params["scale"] = scale
        params["filepath"] = filepath
        params["filterid"] = filterID
        params["cols"] = "0"
        params["rows"] = "0"
        params["cellwidth"] = width
        params["cellheight"] = height
        params["calltype"] = "filteruse"
        params["renderparameters"] = parameters
        params["api_sig"] = self.getApiSignature(params)
        result = self.request(self.SERVER + self.RENDER_URL, params)
        xml = minidom.parse(result)
        url = xml.getElementsByTagName("url")[0].firstChild.data
        finalImage = { "url" : url }
        return finalImage
    
    def getTime(self):
        '''
        (internal) Returns the current server time
        
        @return: Current time on the server
        @rtype: string
        '''
        params = self.defaultParams.copy()
        params["ts"] = int( time.time() )
        params["api_sig"] = self.getApiSignature(params)
        url = self.SERVER + self.GET_TIME_URL
        result = self.request(url, params)
        xml = minidom.parse(result)
        for response in xml.getElementsByTagName("response"):
            for key in response.attributes.keys():
                serverTime = response.getAttribute("servertime")
        return serverTime
        
    def getApiSignature(self, paramsToHash):
        '''
        (Internal) Generates API signature.
        
        @param paramsToHash: Parameters
        @type paramsToHash: dict
        @return: API signature
        @rtype: str
        '''
        keys = paramsToHash.keys()
        keys.sort()
        paramsString = []
        for key in keys:
            paramsString.append(key)
            paramsString.append(paramsToHash[key])
        paramsString = "".join( map(str, paramsString) )
        api_sig = hashlib.md5(self.api_secret + paramsString).hexdigest()
        return api_sig
    
    def request(self, url, params):
        '''
        (Internal) Generates a reequest
        
        @param url: URL
        @type url: str
        @param params: Parameters
        @type params: dict
        @return: Response XML
        @rtype: str   
        '''
        data = urllib.urlencode(params)
        request = urllib2.Request(url, data)
        response = urllib2.urlopen(request)
        return response
    
class FilterInfo(object):
    '''
    (internal) Make a FilterInfo object
    '''
    def __init__(self, label, uid, description, parameters):
        '''
        @param label: label
        @type label: str
        @param uid: uid
        @type uid: string
        @param description: description
        @type description: str  
        @param parameters: parameters
        @type parameters: list 
        '''
        self.label = label
        self.uid = uid
        self.description = description
        self.parameterList = parameters

####
# http://hoisie.com/post/python_sending_a_multipartformdata_request_with_urllib2
####
import mimetools, mimetypes
import stat
from StringIO import StringIO
class Callable:
    '''
    (internal) Used for encoding multipart form data
    '''
    def __init__(self, anycallable):
        self.__call__ = anycallable

# Controls how sequences are uncoded. If true, elements may be given multiple values by
#  assigning a sequence.
doseq = 1

class MultipartPostHandler(urllib2.BaseHandler):
    '''
    (internal) Handles multipart form data
    '''
    handler_order = urllib2.HTTPHandler.handler_order - 10 # needs to run first

    def http_request(self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            v_files = []
            v_vars = []
            try:
                 for(key, value) in data.items():
                     if type(value) == file:
                         v_files.append((key, value))
                     else:
                         v_vars.append((key, value))
            except TypeError:
                systype, value, traceback = sys.exc_info()
                raise TypeError, "not a valid non-string sequence or mapping object", traceback
            if len(v_files) == 0:
                data = urllib.urlencode(v_vars, doseq)
            else:
                boundary, data = self.multipart_encode(v_vars, v_files)
                contenttype = 'multipart/form-data; boundary=%s' % boundary
                if(request.has_header('Content-Type')
                   and request.get_header('Content-Type').find('multipart/form-data') != 0):
                    print "Replacing %s with %s" % (request.get_header('content-type'), 'multipart/form-data')
                request.add_unredirected_header('Content-Type', contenttype)

            request.add_data(data)
        return request

    def multipart_encode(vars, files, boundary = None, buffer = None):
        if boundary is None:
            boundary = mimetools.choose_boundary()
        if buffer is None:
            buffer = StringIO()
        for(key, value) in vars:
            buffer.write('--%s\r\n' % boundary)
            buffer.write('Content-Disposition: form-data; name="%s"' % str(key))
            buffer.write('\r\n\r\n' + str(value) + '\r\n')
        for(key, fd) in files:
            file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
            filename = os.path.basename(fd.name)
            contenttype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            buffer.write('--%s\r\n' % boundary)
            buffer.write('Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (str(key), filename))
            buffer.write('Content-Type: %s\r\n' % contenttype)
            #buffer += 'Content-Length: %s\r\n' % file_size
            fd.seek(0)
            buffer.write('\r\n')
            buffer.write(fd.read())
            buffer.write('\r\n')
        buffer.write('--%s--\r\n\r\n' % boundary )
        return boundary, buffer.getvalue()
    multipart_encode = Callable(multipart_encode)
    https_request = http_request
