
'''Info Header Start
Name : extRoutedBrowser
Author : Wieland@AMB-ZEPH15
Version : 0
Build : 4
Savetimestamp : 2023-07-20T12:41:30.239068
Saveorigin : WebUtils.toe
Saveversion : 2022.28040
Info Header End'''
from urllib import request
import exceptions

from request import Request
from response import Response
from cookie import Cookie

class RoutedBrowser:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		#self.Route_Definition = mod( self.ownerComp.par.Routes.eval().path ).routes
		self.Exceptions = exceptions
		self.Cookie = Cookie

	@property
	def Route_Definition(self):
		return getattr( self.ownerComp.op("repo_maker").Repo.module, "routes", {} )
	
	@property
	def Middleware_Definition(self):
		return getattr( self.ownerComp.op("repo_maker").Repo.module, "midllewares", [] )

	def Create_Routes(self):
		self.ownerComp.op("repo_maker").Create_Repo()
		
	def handle_request( self, td_request, td_response ):
		response_object = Response( td_response )
		request_object = Request( td_request )
		params, route_handler = self.find_route( request_object )
		request_object.params = params

		try:
			for middleware in route_handler.get("middleware", []) + self.Middleware_Definition:
				middleware( request_object, response_object, self.ownerComp )
			response_object.statuscode = 200
			response_object.statusreason = "Ok"

			route_handler["handler"](request_object, response_object, self.ownerComp)
			
		except Exception as e:
			code = exceptions.exception_dict.get( type(e), 500)
			response_object.statuscode 		= code
			response_object.statusreason 	= str(e)
			response_object.data			= e
		
		return response_object._parsed_response()


	def find_route(self, request):
		if request.method in self.Route_Definition:	
			for uri in self.Route_Definition[request.method]:
				route_parameter = self.routecheck( request.uri[1:].split('/'), uri[1:].split('/'), {} )
				if route_parameter is  None: continue
				return route_parameter, self.Route_Definition[request.method][uri]
		
		default 	= self.Route_Definition.get("DEFAULT", None)
		if default: return {}, default
		raise exceptions.NotFound( f"Could not find {request.method}:{request.uri}")


	def routecheck(self,request_list, route_list, parameter):
		#check if they are the same length. If not abort instantly!
		if len(route_list) != len(request_list): return None
		#check if there is even stuff available. If not return the parameter
		elif not len(route_list): return parameter 

		#get the current element and init new parameterdict
		request_set = request_list[0]
		route_set = route_list[0]
		update_parameter = {**parameter}
		#check if we are having a parameter set
		if      route_set.startswith(":") : update_parameter.update(  {route_set[1:] : request_set} )
		#if not, check if we are having an overlap
		elif route_set != request_set: return None
		return self.routecheck(request_list[1:], route_list[1:], update_parameter)
	