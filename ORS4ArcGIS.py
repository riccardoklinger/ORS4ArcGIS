import arcpy
import ctypes
import urllib.request
import json

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="From Address",
            name="in_value_from",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param1 = arcpy.Parameter(
            displayName="To Address",
            name="in_value_to",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        params = [param0, param1]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
	
    def geocode(locationstring):
        url = "https://api.openrouteservice.org/geocoding?query=" + locationstring + "&lang=de&limit=20&api_key=58d904a497c67e00015b45fcc8ce8f9f73cb4a2c6adf73a107dcbd4c"
        webURL=urllib.request.urlopen(url)
        data = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        response = json.loads(data.decode(encoding))
        coordinates = response["features"][0]["geometry"]["coordinates"]
        return coordinates
    def execute(self, parameters, messages):
        ###getting parameters###
        fromAddress = parameters[0].valueAsText
        toAddress = parameters[1].valueAsText
        ###getting start location accroding to most relevant hit###
        start = Tool.geocode(fromAddress)
        ###getting stop location accroding to most relevant hit###
        stop = Tool.geocode(toAddress)
        ###getting route###
        
		###coordinates to log###
        messages.addMessage("Start coordinates are " + str(start[0]) + ";" + str(start[1]))
        MessageBoxW = ctypes.windll.user32.MessageBoxW
        MessageBoxW(0, u'Hello', "", 0)
        return
