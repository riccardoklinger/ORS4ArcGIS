import arcpy
import ctypes
import urllib.request
from urllib.parse import quote  
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
		param2 = arcpy.Parameter(
			displayName ='Routing Profile',
			name ='profile',
			datatype='GPString',
			parameterType='Required',
			direction='Input')
		param2.filter.type = "ValueList"
		param2.filter.list = ["driving-car", "cycling-regular" , "foot-walking"]
		param2.value = param2.filter.list[0]
		param3 = arcpy.Parameter(
			displayName ='Routing Preference',
			name ='preference',
			datatype='GPString',
			parameterType='Required',
			direction='Input')
		param3.filter.type = "ValueList"
		param3.filter.list = ["fastest", "shortest"]
		param3.value = param3.filter.list[0]
		params = [param0, param1, param2, param3]
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
		urlraw = "https://api.openrouteservice.org/geocoding?query=" + locationstring + "&lang=de&limit=20&api_key=58d904a497c67e00015b45fcc8ce8f9f73cb4a2c6adf73a107dcbd4c"
		url=quote(urlraw, safe="%/:=&?~#+!$,;'@()*[]")
		webURL=urllib.request.urlopen(url)
		data = webURL.read()
		encoding = webURL.info().get_content_charset('utf-8')
		response = json.loads(data.decode(encoding))
		coordinates = response["features"][0]["geometry"]["coordinates"]
		return coordinates
		
	def getRoute(start,stop,routeParams, messages):
		coordinates = str(start[0]) + "," + str(start[1]) + "|" + str(stop[0]) + "," +str(stop[1])
		urlraw = "https://api.openrouteservice.org/directions?coordinates=" + coordinates 
		urlraw += "&profile=" + routeParams[0] + "&preference=" + routeParams[1] + "&units=m&language=en&geometry=true&geometry_format=geojson&geometry_simplify=false&instructions=false&instructions_format=text&maneuvers=false&elevation=false&optimized=false&api_key=58d904a497c67e00015b45fcc8ce8f9f73cb4a2c6adf73a107dcbd4c"
		url=quote(urlraw, safe="%/:=&?~#+!$,;'@()*[]")
		#messages.addMessage(url)
		webURL=urllib.request.urlopen(url)
		data = webURL.read()
		encoding = webURL.info().get_content_charset('utf-8')
		response = json.loads(data.decode(encoding))
		data = response["routes"]
		return data
		
	def execute(self, parameters, messages):
		###getting parameters###
		fromAddress = parameters[0].valueAsText
		toAddress = parameters[1].valueAsText
		###getting start location accroding to most relevant hit###
		start = Tool.geocode(fromAddress)
		###getting stop location accroding to most relevant hit###
		stop = Tool.geocode(toAddress)
		###getting route###
		routeParams = [parameters[2].valueAsText, parameters[3].valueAsText]
		route = Tool.getRoute(start, stop, routeParams, messages)
		messages.addMessage("Distance: " + str(route[0]["summary"]["distance"]) + "; Duration: " +  str(route[0]["summary"]["duration"]))
		###coordinates to log###
		MessageBoxW = ctypes.windll.user32.MessageBoxW
		MessageBoxW(0, u'Hello', "", 0)
		return
