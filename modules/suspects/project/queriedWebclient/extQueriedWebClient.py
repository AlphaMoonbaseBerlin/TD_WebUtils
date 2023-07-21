'''Info Header Start
Name : extQueriedWebClient
Author : Wieland@AMB-ZEPH15
Version : 0
Build : 10
Savetimestamp : 2023-07-21T19:57:15.560048
Saveorigin : WebUtils.toe
Saveversion : 2022.28040
Info Header End'''
import json
import urllib.parse
import requests
import request
import response
import quriedwebclient_exceptions
from cookie import Cookie

def default_callback(request, response, server):
	return None
class extQueriedWebClient:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp 			= ownerComp
		self.requests 			= []
		self.active 			= False
		self.current_request 	= None

		self.Processing 		= tdu.Dependency( False )
		self.Exceptions = quriedwebclient_exceptions
		self.Cookie = Cookie
		self.Request_Class = request.Request
		self.Response_Class = response.Response
	
	@property 
	def server(self):
		return self.ownerComp.par.Server.eval()
	
	def Timeout(self):
		self.ownerComp.op("webclient").par.stop.pulse()
		self.ownerComp.op("callbackManager").Do_Callback("onTimeout", self.current_request, self.ownerComp)

		self.current_request = None
		self.active = False
		self.check_query()
	
	def check_query(self):
		
		if self.active: return
		self.ownerComp.op("timeout").par.initialize.pulse()
		if not self.requests: 
			self.Processing.val = False
			return self.ownerComp.op("callbackManager").Do_Callback("onQueryEmpty", self.ownerComp)
		
		self.Processing.val = True
		self.active = True
		self.current_request = self.requests.pop(0)
		run( "me.ext.extQueriedWebClient.trigger_request()", fromOP=self.ownerComp, delayFrames = 1)
		return
		
	def parse_body(self, data):
		return json.dumps( data ) if type(data) is dict else data
	
	
	def read_body(self, data):
		try:
			encoded_data = data.decode()
		except: 
			return data
		try:
			
			return json.loads(encoded_data)
		except:
			return encoded_data
		
	def trigger_request(self):
		self.ownerComp.op("timeout").par.start.pulse()
		self.ownerComp.op("webclient").request(
					  self.current_request._get_url(),
					  self.current_request._get_method(),
			header 	= self.current_request._get_header(),
			data 	= self.current_request._get_data()
		)
	
	def parse_response(self, status, headerDict, data):
		statusCode = status["code"]
		statusReason = status["message"]
		
		current_request = self.current_request
		self.active = False
		self.current_request = None
		
		response_item = response.Response(
			statusCode, statusReason, headerDict, data
		)

		if statusCode >= 400:
			exception = quriedwebclient_exceptions.get( statusCode )
			
			self.ownerComp.op("callbackManager").Do_Callback("onError", current_request, 
																		response_item,
																		exception, 
																		self.ownerComp )
		else:
			self.ownerComp.op("callbackManager").Do_Callback("onResponse" , current_request,
																			response_item,
																			self.ownerComp )
			
			try:
				current_request.callback( current_request, response_item, self.ownerComp )
			except Exception as e:
				debug("Error in Request_Callback", e, current_request)
			
		self.check_query()
		return
	
	def MultipartFormData(self, dictionary):
		return requests.Request("POST", "https://thisdoesnotexist.azua", files = dictionary).prepare().body
	
	def _read_header(self):
		if self.ownerComp.par.Header.eval():
			return { row[0].val : row[1].val for row in self.ownerComp.par.Header.eval().rows() }
		return {}

	def QueryRequest(self, request_object):
		request_object.header.update( self._read_header() )
		self.requests.append( request_object )
		self.check_query()
		return request_object

	
	def Get(self, endpoint, params = {}, header = {}, cookies = [], callback = default_callback):
		return self.QueryRequest( 
			request.Request(
				self.server,
				"GET",
				uri = endpoint,
				query = params,
				header = header,
				cookies = cookies,
				data = None,
				callback = callback
			)
		 )
			
	def Post(self, endpoint, params = None, header = {}, cookies = [], data = None, callback = default_callback):
		method = "POST"
		return self.QueryRequest( 
			request.Request(self.server,method,uri = endpoint,query = params,header = header,cookies = cookies,data = data,callback = callback)
		 )
	
	def Put(self, endpoint, params = None, header = {}, cookies = [], data = None, callback = default_callback):
		method = "PUT"
		return self.QueryRequest( 
			request.Request(self.server,method,uri = endpoint,query = params,header = header,cookies = cookies,data = data,callback = callback)
		 )
	
	def Patch(self, endpoint, params = None, header = {}, cookies = [], data = None, callback = default_callback):
		method = "PATCH"
		return self.QueryRequest( 
			request.Request(self.server,method,uri = endpoint,query = params,header = header,cookies = cookies,data = data,callback = callback)
		 )
		
	def Delete(self, endpoint, params = None, header = {}, cookies = [], data = None, callback = default_callback):
		method = "DELETE"
		return self.QueryRequest( 
			request.Request(self.server,method,uri = endpoint,query = params,header = header,cookies = cookies,data = data,callback = callback)
		 )
	
	def Search(self, endpoint, params = None, header = {}, cookies = [], data = None, callback = default_callback):
		method = "SEARCH"
		return self.QueryRequest( 
			request.Request(self.server,method,uri = endpoint,query = params,header = header,cookies = cookies,data = data,callback = callback)
		 )