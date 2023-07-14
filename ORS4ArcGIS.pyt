import arcpy
import ctypes
import requests
import json

class Toolbox(object):
	def __init__(self):
		"""Define the toolbox (the name of the toolbox is the name of the
		.pyt file)."""
		self.label = "OpenRoute+ Toolbox"
		self.alias = "OpenRoute+ Toolbox"

		# List of tool classes associated with this toolbox
		self.tools = [directions, isochrones]


class directions(object):
	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "Routenfindung"
		self.description = "Ein Tool zur Ermittlung von A-B Routen"
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
		
	def getRoute(routeParams, messages):
		#coordinates = str(start[0]) + "," + str(start[1]) + "|" + str(stop[0]) + "," +str(stop[1])
		#urlraw = "https://api.openrouteservice.org/directions?coordinates=" + coordinates 
		#urlraw += "&profile=" + routeParams[0] + "&preference=" + routeParams[1] + "&units=m&language=en&geometry=true&geometry_format=geojson&geometry_simplify=false&instructions=false&instructions_format=text&maneuvers=false&elevation=false&optimized=false&api_key=58d904a497c67e00015b45fcc8ce8f9f73cb4a2c6adf73a107dcbd4c"
		#url=quote(urlraw, safe="%/:=&?~#+!$,;'@()*[]")
		url='http://sg.geodatenzentrum.de/web_ors/v2/directions/driving-car/geojson'
		#header =  -H 'Content-Type: application/json; charset=utf-8' -H 'Accept: application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8'
		data = {"coordinates":[[8.83098,49.89201],[8.92367,49.8884]]}
		#data = parse.urlencode(data).encode()
		proxies = {"http":"http://10.226.2.64:80", "https":"http://10.226.2.64:80"}
		header = {"Content-Type": "application/json; charset=utf-8",
	    			"Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8"}

		messages.addMessage(url)
		#req =  request.Request(url,data = data)
		#req.set_proxy(proxies["http"], 'http')
		#req.set_proxy(proxies["https"], 'https')
		#resp = request.urlopen(req)
		req = requests.post(url, proxies=proxies, data=data, headers= header)
		messages.addMessage(req.text)

		#response = json.loads(resp)
		data = response["routes"]
		return data
		
	def execute(self, parameters, messages):
		###getting parameters###
		fromAddress = parameters[0].valueAsText
		toAddress = parameters[1].valueAsText
		###getting start location accroding to most relevant hit###
		#start = Tool.geocode(fromAddress)
		###getting stop location accroding to most relevant hit###
		#stop = Tool.geocode(toAddress)
		###getting route###
		routeParams = [parameters[2].valueAsText, parameters[3].valueAsText]
		route = Tool.getRoute( routeParams, messages)
		messages.addMessage("Distance: " + str(route[0]["summary"]["distance"]) + "; Duration: " +  str(route[0]["summary"]["duration"]))
		###coordinates to log###
		MessageBoxW = ctypes.windll.user32.MessageBoxW
		MessageBoxW(0, u'Hello', "", 0)
		return


class isochrones(object):
	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "Erreichbarkeitsanalyse"
		self.description = "Ein Tool zur Ermittlung von Isocrhonen/Erreichbarkeiten"
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
		
	def getRoute(routeParams, messages):
		#coordinates = str(start[0]) + "," + str(start[1]) + "|" + str(stop[0]) + "," +str(stop[1])
		#urlraw = "https://api.openrouteservice.org/directions?coordinates=" + coordinates 
		#urlraw += "&profile=" + routeParams[0] + "&preference=" + routeParams[1] + "&units=m&language=en&geometry=true&geometry_format=geojson&geometry_simplify=false&instructions=false&instructions_format=text&maneuvers=false&elevation=false&optimized=false&api_key=58d904a497c67e00015b45fcc8ce8f9f73cb4a2c6adf73a107dcbd4c"
		#url=quote(urlraw, safe="%/:=&?~#+!$,;'@()*[]")
		url='http://sg.geodatenzentrum.de/web_ors/v2/directions/driving-car/geojson'
		#header =  -H 'Content-Type: application/json; charset=utf-8' -H 'Accept: application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8'
		data = {"coordinates":[[8.83098,49.89201],[8.92367,49.8884]]}
		#data = parse.urlencode(data).encode()
		proxies = {"http":"http://10.226.2.64:80", "https":"http://10.226.2.64:80"}
		header = {"Content-Type": "application/json; charset=utf-8",
	    			"Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8"}

		messages.addMessage(url)
		#req =  request.Request(url,data = data)
		#req.set_proxy(proxies["http"], 'http')
		#req.set_proxy(proxies["https"], 'https')
		#resp = request.urlopen(req)
		req = requests.post(url, proxies=proxies, data=data, headers= header)
		messages.addMessage(req.text)

		#response = json.loads(resp)
		data = response["routes"]
		return data
		
	def execute(self, parameters, messages):
		###getting parameters###
		fromAddress = parameters[0].valueAsText
		toAddress = parameters[1].valueAsText
		###getting start location accroding to most relevant hit###
		#start = Tool.geocode(fromAddress)
		###getting stop location accroding to most relevant hit###
		#stop = Tool.geocode(toAddress)
		###getting route###
		routeParams = [parameters[2].valueAsText, parameters[3].valueAsText]
		route = Tool.getRoute( routeParams, messages)
		messages.addMessage("Distance: " + str(route[0]["summary"]["distance"]) + "; Duration: " +  str(route[0]["summary"]["duration"]))
		###coordinates to log###
		MessageBoxW = ctypes.windll.user32.MessageBoxW
		MessageBoxW(0, u'Hello', "", 0)
		return
