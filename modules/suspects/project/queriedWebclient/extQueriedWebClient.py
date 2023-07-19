
'''Info Header Start
Name : extQueriedWebClient
Author : Wieland@AMB-ZEPH15
Version : 0
Build : 5
Savetimestamp : 2023-07-19T21:26:15.570396
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''
import json
import urllib.parse
import requests
import quriedwebclient_exceptions

class extQueriedWebClient:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.requests = []
		self.active = False
		self.current_request = None
		self.ownerComp.op("status").par.value0 = 0
		self.Processing = tdu.Dependency( False )
		self.Exceptions = quriedwebclient_exceptions
	
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
			self.ownerComp.op("status").par.value0 = 0
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
			
	def parse_header(self, header, data):
		copy_header = header.copy()
		if self.ownerComp.par.Header.eval():
			for row in self.ownerComp.par.Header.eval().rows():
				copy_header[row[0].val] = row[1].val
				
		if type(data) is dict: copy_header["Content-Type"] =  "application/json"
		return copy_header
		
	def trigger_request(self):
		self.ownerComp.op("timeout").par.start.pulse()

		self.ownerComp.op("status").par.value0 = 1

		self.ownerComp.op("webclient").request(
									self.current_request["url"],
									self.current_request["method"],
			header = self.parse_header(self.current_request["header"], self.current_request["body"]),
			data = self.parse_body( self.current_request["body"] )
		)
		
		
	def join_endpoint(self, endpoint):
		return urllib.parse.urljoin( self.server.rstrip("/") + "/", endpoint.lstrip("/") )	
		
	def add_query(self, url, params):
		if not params: return url
		
		url_parse = urllib.parse.urlparse(url)
		query = url_parse.query
		url_dict = dict(urllib.parse.parse_qsl(query))
		url_dict.update(params)
		url_new_query = urllib.parse.urlencode(url_dict)
		url_parse = url_parse._replace(query=url_new_query)
		new_url = urllib.parse.urlunparse(url_parse)
		return new_url
	
	def parse_response(self, statusCode, headerDict, data):
		
		parsed_data = self.read_body( data )
		current_request = self.current_request
		self.active = False
		self.current_request = None
		response_dict = { 	"statuscode" : statusCode,
							"body" : parsed_data, 
							"header" : headerDict }

		if statusCode >= 400:
			exception = quriedwebclient_exceptions.get( statusCode )
			
			self.ownerComp.op("callbackManager").Do_Callback("onError", current_request, 
																		 response_dict, 
																		 exception, 
																		 self.ownerComp )
		else:
			self.ownerComp.op("callbackManager").Do_Callback("onResponse" , current_request,
																			response_dict,
																			self.ownerComp )
			
			try:
				current_request["callback"]( current_request, response_dict, self.ownerComp )
			except Exception as e:
				debug("Error in Request_Callback", e, current_request)
			
		self.check_query()
		return
	
	def MultipartFormData(self, dictionary):
		return requests.Request("POST", "https://thisdoesnotexist.azua", files = dictionary).prepare().body
	
	def QueryRequest(self, request_dict):
		self.requests.append( request_dict )
		self.check_query()
		return request_dict

	
	def Get(self, endpoint, params = None, header = {}, callback = lambda result: None):
		return self.QueryRequest( {
			"method" 	: "GET",
			"url"		: self.add_query( self.join_endpoint( endpoint ), params ),
			"header"	: header,
			"body"		: None,
			"params"	: params,
			"callback"	: callback } )
			
	def Post( self, endpoint, params = None, header = {}, callback = lambda result: None, data = None ):
		return self.QueryRequest( {
			"method" 	: "POST",
			"url"		: self.add_query( self.join_endpoint( endpoint ), params ),
			"header"	: header,
			"body"		: data,
			"params"	: params,
			"callback"	: callback } )
			
	def Put( self, endpoint, params = None, header = {}, callback = lambda result: None, data = None ):
		return self.QueryRequest( {
			"method" 	: "PUT",
			"url"		: self.add_query( self.join_endpoint( endpoint ), params ),
			"header"	: header,
			"body"		: data,
			"params"	: params,
			"callback"	: callback } )

	def Patch( self, endpoint, params = None, header = {}, callback = lambda result: None, data = None ):
		return self.QueryRequest( {
			"method" 	: "PATCH",
			"url"		: self.add_query( self.join_endpoint( endpoint ), params ),
			"header"	: header,
			"body"		: data,
			"params"	: params,
			"callback"	: callback } )
			
		
	def Delete( self, endpoint, params = None, header = {}, callback = lambda result: None, data = None ):
		return self.QueryRequest( {
			"method" 	: "DELETE",
			"url"		: self.add_query( self.join_endpoint( endpoint ), params ),
			"header"	: header,
			"body"		: data,
			"params"	: params,
			"callback"	: callback } )
		
		
		
		