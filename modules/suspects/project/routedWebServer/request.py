
'''Info Header Start
Name : request
Author : Wieland@AMB-ZEPH15
Version : 0
Build : 3
Savetimestamp : 2023-07-19T21:23:41.062947
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''
import json
import exceptions
from dataclasses import dataclass

@dataclass
class Request:
	method : str
	header : dict
	uri    : str
	params : dict
	query  : dict
	data   : any
	cookies : dict
	_td_request : any

	def __init__(self, td_request):
		self._td_request = td_request
		self.method 	= td_request["method"]
		self.header 	= td_request.get("header", {})
		self.uri 		= td_request["uri"]
		self.cookies	= self._parse_cookies( td_request.get("Cookie", "") )
		self.query 		= td_request["pars"]
		self.data 		= self.try_parse_data( td_request["data"] )
		self.params 	= {}
		
	def _parse_cookies(self, cookiestring):
		cookiestrings = cookiestring.split(";")
		return_dict = {}
		for key_value_string in cookiestrings:
			if not key_value_string: continue
			key, value = key_value_string.split("=")
			return_dict[key] = value
		return return_dict

	def try_parse_data(self, data):
		try:
			return json.loads( data )
		except:
			return data


